

# -*- coding: utf-8 -*-
"""

@Filename : worker lambda module
@created :  Dec 7 11:42 2020
@project: lambda-exchange-tracker
@author : Nikkhil Butola
"""

import asyncio
import glob
import json
import logging
import mimetypes
import os
import traceback
import uuid
from datetime import datetime, timedelta
from io import BytesIO

import boto3
import pytz
import distutils
import re
from io import BytesIO

from src import constants
from src import test_events as events
from src.utils import helper
from src.utils import exchange_scraper as exchange
from src.models.pydantic_serializer import EventScrapeData, CurrencyExchangeModel
from src.databases import ExchangeDynamoDB

# setting the logger stack
logging.getLogger().setLevel(logging.INFO)
loggingFormat = "[%(filename)s: %(lineno)s- %(funcName)11s() ] %(asctime)s: %(name)s:%(levelname)s %(message)s"
logging.basicConfig(format=loggingFormat)
logger = logging.getLogger(__name__)


table_name = os.getenv("table_name", constants.table_name)
API_FETCH_CURRENCY_EXCHANGE = "/api/v1/kaizen/fetch-currency-exchange/generate"
req_id = uuid.uuid1()

__dynamoDB = ExchangeDynamoDB(table_name=table_name)


def async_lambda_handler(event, context):
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(lambda_handler(event, context))

    except Exception:
        logger.error(traceback.format_exc())
        logger.info("logging the async handler exception ...")


async def lambda_handler(event, context):
    stage = context.invoked_function_arn.split(":")[-1]
    logger.info(f"logging the stage event  : {event = } ...")
    errorMessage = "Internal Server Error"

    try:
        logger.info(f"logging the event : {event = } ...")
        if API_FETCH_CURRENCY_EXCHANGE in event.get("path", ""):
            try:
                logger.info("Fetch currency exchange and changed rate API called ...")
                params = event.get("queryStringParameters", {})
                date_param = params.get("date-param", datetime.now(pytz.timezone("Asia/Kolkata")).date().isoformat()),

                __fetch_exchange_response = __dynamoDB.currency_alloc.get_latest_currency_exchange_result(
                    date=date_param[0],
                )

                return {
                    "statusCode": 200,
                    "body": json.dumps(
                        {
                            "response": __fetch_exchange_response.dict()["metadata"],
                            "requestMetaData": {
                                "requestId": str(req_id),
                                "errorMessage": "",
                                "statusCode": 200,
                                "version": "v1",
                                "clientId": "Kaizen",
                                "timestamp": helper.get_iso_timestamp(timezone="UTC"),
                            },
                        }
                    ),
                }

            except Exception:
                logger.error(f"error with {event = } and {context = }")
                logger.error(traceback.format_exc())
                return {
                    "statusCode": 500,
                    "body": json.dumps(
                        {
                            "requestMetaData": {
                                "requestId": req_id,
                                "errorMessage": "Internal Server error",
                                "statusCode": 500,
                                "version": "v1",
                                "clientId": "Kaizen",
                                "timestamp": helper.get_iso_timestamp(timezone="UTC"),
                            },
                        }
                    ),
                }

        # scheduling the cron lambda worker for web-scraping
        if event.get("source", None) == "aws.events":
            logger.info("Everyday cron job called !!")
            start = datetime.now(pytz.timezone("Asia/Kolkata"))

            results: CurrencyExchangeModel = await exchange.perform_scraping_handling(
                event_params=EventScrapeData(
                    event_id=str(uuid.uuid1()),
                    website_uri=constants.scrape_website_uri,
                ),

            )

            # perform result serialization and store within DynamoDB with - SK -> SCRAPECURRENCY
            __dynamoDB.currency_alloc.save_currency_exchange_result(
                result=results
            )

    except Exception as error:
        logger.error(f"{error =} with trace: {traceback.format_exc()}")
        logger.info(f"{event = }")
        raise Exception(f"Failed to load object: {event =} with {error =}")


if __name__ == "__main__":

    class Context:
        invoked_function_arn = "test:dev"

    print(
        async_lambda_handler(
            event=events.api_currency_exchange_event, context=Context()
        )
    )
    print("Lambda successfully executed, signing off !!!")
