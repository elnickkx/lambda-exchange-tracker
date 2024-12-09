# -*- coding: utf-8 -*-
"""

@Filename : exchange scrape handler
@created :  Dec 7 11:42 2020
@project: lambda-exchange-tracker
@author : Nikkhil Butola
"""

import logging
import aiofiles

from bs4 import BeautifulSoup, Tag
import aiohttp
import os
import random
from src.models.pydantic_serializer import EventScrapeData, CurrencyExchange, CurrencyExchangeModel
from collections import OrderedDict
import typing
import uuid
import traceback
import json
import pytz
import pathlib
from datetime import datetime, timedelta
from src import constants
from src.utils.decorators import retry_handling
from src.databases import ExchangeDynamoDB

## configure the base logger settings for logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
loggingFormat = "[%(filename)s: %(lineno)s- %(funcName)11s() ] %(asctime)s: %(name)s:%(levelname)s %(message)s"
logging.basicConfig(format=loggingFormat)

__all__ = ["perform_scraping_handling", "__init_website_uri"]

# setting the pd dataframe maximum width
__init_website_uri = constants.scrape_website_uri


@retry_handling.perform_retry(max_retries=3, wait_time=5)
async def __perform_query_search(*, session: aiohttp, search_href: str) -> typing.Union[None, Tag]:
    ## handling to scrape persist information from INIT_WEBSITE_URI
    soup_query_response: typing.Union[None, Tag] = None
    try:
        async with session.get(search_href) as scrape_response:
            if scrape_response.status not in [500]:
                scrape_response = await scrape_response.read()

                # scrape_authorisation = urlopen(__init_request).read()  # performing web authorisation for request uri
                soup_query_response = BeautifulSoup(
                    scrape_response.decode('utf-8'),
                    'html.parser'
                )  # conceive the HTML format response on scraped website

            else:
                raise Exception("Mislead website scrape uri, performing decoupling mechanism ...")

    except Exception:
        logger.error(traceback.format_exc())

    else:
        return soup_query_response


async def __fetch_and_parse_response(date: datetime.date):
    __dynamoDB = ExchangeDynamoDB(table_name=constants.table_name)
    _parsed_map = dict()

    try:
        if response := __dynamoDB.currency_alloc.get_latest_currency_exchange_result(
                date=date
        ):
            for _iter in response.metadata:
                _parsed_map[_iter.symbol] = _iter.spot_rate

            return _parsed_map

    except Exception:
        return _parsed_map

    return _parsed_map


async def __check_exchange_fluctuation(
        data: typing.Dict[str, str],
        symbol: str,
        curr_spot_rate: str
) -> str:
    if not data:
        return "0.00"

    try:
        if symbol in data:
            return str(
                round(float(curr_spot_rate) - float(data.get(symbol, "0.00")), 4)
            )

    except Exception:
        logger.error(traceback.format_exc())
        raise Exception

    return "0.00"


async def ___execute_query_scraper_builder(
        *,
        session: aiohttp, soup_query_response: Tag,
        __pg_product_mapper: typing.List[typing.Dict],
        page_idx: typing.Union[None, int] = 1,
        **kwargs
) -> typing.Dict[str, typing.List[typing.Dict[str, str]]]:
    try:
        if not soup_query_response:
            return []

        _metadata = dict()
        # caution handlin' to scrape all enlist currency exchanges,
        # and deduce multi-FOR handlin -> WHILE operator sujective
        if scraped_product_info := soup_query_response.findAll("table", class_=["forextable"]):
            try:
                __product_iterator: typing.Union[None, typing.Iterator] = iter(scraped_product_info)

            except Exception:
                raise Exception

        else:
            __product_iterator = None

        try:
            paginator_scraping: bool = True
            curr_date = datetime.now(pytz.timezone("Asia/Kolkata"))
            prev_date = (curr_date - timedelta(days=1)).replace(hour=0, minute=0, second=0).date()
            populate_data = None

            if _fetch_prev_response := await __fetch_and_parse_response(date=prev_date):
                _fetch_prev_response = _fetch_prev_response

            # fetch the scraped result from DynamoDB for prev_date
            _table_body: typing.Union[None, Tag] = None
            while _table_body := __product_iterator and next(
                    __product_iterator, None
            ):
                _table_rows: typing.Union[None, typing.Iterator] = iter(_table_body.tbody.findAll('tr'))
                while _row := _table_rows and next(
                        _table_rows, None
                ):
                    __exchange_hash_mapper = OrderedDict(index=str(uuid.uuid1()))
                    r_cols: typing.List[None, Tag] = _row.findAll('td')  # table data tag
                    __exchange_hash_mapper["symbol"] = symbol = r_cols[0].text.strip()
                    __exchange_hash_mapper["currency"] = r_cols[1].text.strip()
                    __exchange_hash_mapper["spot_rate"] = spot_rate = r_cols[2].text.strip()
                    __exchange_hash_mapper["fluctuation"] = await __check_exchange_fluctuation(
                        data=_fetch_prev_response, symbol=symbol, curr_spot_rate=spot_rate,
                    ) if _fetch_prev_response else "0.00"

                    # add the entity to final currency mapper
                    __pg_product_mapper.append(
                        CurrencyExchange(
                            **__exchange_hash_mapper
                        )
                    )

            _metadata = CurrencyExchangeModel(
                metadata=__pg_product_mapper
            )

            # update the fetched scraped response to DynamoDB `currency_exchange` table
            # SK -> SCRAPECURRENCY

        except (StopIteration, Exception):
            logger.error(traceback.format_exc())

    except Exception:
        logger.error(traceback.format_exc())

    else:
        return _metadata


async def perform_scraping_handling(
        event_params: EventScrapeData,
        fetched_json_data: typing.Union[None, typing.List[
            typing.Dict[str, typing.Union[str, int, float, typing.Dict[str, typing.Union[int, str]]]]]] = None,
) -> typing.Union[CurrencyExchangeModel, typing.Dict[str, typing.Any]]:
    logger.info(f"Performing scraping event with metadata as {event_params} ...")

    try:
        """
            1. initiate Request mode on event-scraping uri
            2. once the response captured, forward the page-response to restricted query executor
            3. write the builder query response to JSON file, and yield the local blob storage address
                4.1 for file revision history record, file_name as `datetime stamp + event_id[uuid].json`
                    to maintain the unique records for rewrite

        """

        if not event_params.website_uri:
            raise Exception

        __pg_product_mapper: typing.List = list()
        __blob_filename: str = "".join([str(datetime.utcnow()), "-", str(event_params.event_id), ".json"])

        async with aiohttp.ClientSession(headers=constants.AGENT_HEADER, timeout=aiohttp.ClientTimeout(20)) as session:
            if bs4_query_response := await __perform_query_search(
                    session=session, search_href=event_params.website_uri
            ):
                __final_mapper_response = await ___execute_query_scraper_builder(
                    session=session,
                    soup_query_response=bs4_query_response,
                    __pg_product_mapper=__pg_product_mapper,
                    ## modifying the kwargs params to perform scrape-query event on proxy-search string
                    **{
                        "search_href": __init_website_uri if __init_website_uri else event_params.website_uri,
                        "event_id": event_params.event_id,
                    }
                )
                del __pg_product_mapper

    except Exception:
        logger.error(traceback.format_exc())
        return dict(status_code=404, content={"error": "Invalid event metadata to initiate scraping-event ..."})

    else:
        return __final_mapper_response
