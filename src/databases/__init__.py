# -*- coding: utf-8 -*-
"""

@Filename : module initializer
@created :  Dec 7 11:42 2020
@project: lambda-exchange-tracker
@author : Nikkhil Butola
"""

import boto3
import localstack.sdk.aws

from databases.dynamodb import _ExchangeSubTable

client = localstack.sdk.aws.AWSClient()

__all__ = ["ExchangeDynamoDB"]


class ExchangeDynamoDB:
    def __init__(self, *,  table_name):
        # initializing the DynamoDB as localstack hosted service
        self._client = boto3.resource(
            "dynamodb",
            endpoint_url=client.configuration.host,
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )

        self._table_name = table_name
        self._table = self._client.Table(table_name)
        self.currency_alloc = _ExchangeSubTable(table=self._table)
