# -*- coding: utf-8 -*-
"""

@Filename : DynamoDB integration helper
@created :  Dec 7 11:42 2020
@project: lambda-exchange-tracker
@author : Nikkhil Butola
"""
import datetime
import uuid
import typing
import brotli
import json

from pydantic.main import BaseModel
from boto3.dynamodb.conditions import Key
from src.databases.utils import DynamoDBBase, wrap_model, handle_decimals
from src.utils.helper import get_iso_timestamp
from src.constants import DYNAMODB_SORT_KEY as _SK, DYNAMODB_PARTITION_KEY as _PK
from src.models.pydantic_serializer import CurrencyExchangeModel


class ModelResult(DynamoDBBase):
    pk: str
    sk: str
    identifier: str
    is_compressed: bool = False
    result: typing.Union[CurrencyExchangeModel, bytes]


class _ExchangeSubTable:
    """
    AWS dynamoDB table localstack arn: arn:aws:dynamodb:us-east-1:000000000000:table/local_currency_exchange
    aws --endpoint-url=http://localhost:4566 dynamodb list-tables
    """

    def __init__(self, *, table):
        self._table = table
        self._pk = "CURRENCY"

    @wrap_model(ModelResult)
    def save_currency_exchange_result(self, *, result: typing.Union[CurrencyExchangeModel, bytes]):
        obj = {
            _PK: self._pk,
            _SK: f"SCRAPED_EXCHANGE#{get_iso_timestamp()}",
            "identifier": str(uuid.uuid4()),
            "is_compressed": isinstance(result, bytes),
            "result": result
            if isinstance(result, bytes)
            else handle_decimals(result.dict()),
        }

        self._table.put_item(Item=obj)
        return obj

    @wrap_model(CurrencyExchangeModel)
    def get_latest_currency_exchange_result(self, *, date: datetime.date):
        results = self._table.query(
            KeyConditionExpression=(
                    Key(_PK).eq(self._pk) & Key(_SK).begins_with(f"SCRAPED_EXCHANGE#{date}T")
            ),
            ScanIndexForward=False,
            Limit=1,
        )

        items = results["Items"]

        if len(items) == 0:
            raise ValueError(f"No recent scrapped result found for date '{date}'")

        _response_obj = items[0]
        json_string = (
            brotli.decompress(_response_obj["result"].value).decode("utf-8")
            if _response_obj["is_compressed"]
            else json.dumps(_response_obj["result"])
        )
        _response_obj = json.loads(json_string)

        return _response_obj
