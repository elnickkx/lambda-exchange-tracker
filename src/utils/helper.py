
# -*- coding: utf-8 -*-
"""

@Filename : Utility helper
@created :  Dec 7 11:42 2020
@project: lambda-exchange-tracker
@author : Nikkhil Butola
"""

import base64
import copy
import datetime
import glob
import json
import logging
import math
import os
import re
import shutil
import traceback
import typing
import uuid
import zipfile
from io import BytesIO

import boto3
import pandas as pd
import pytz
import requests
from collections import OrderedDict

# from constants import policy_columns
from dateutil import parser

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)
__middleware_s3_client = boto3.client("s3")
__s3_resource = boto3.resource("s3")


def get_iso_timestamp(timezone="Asia/Kolkata") -> str:
    # datetime.now(timezone.utc).isoformat()
    tz = pytz.timezone(timezone)
    timestamp = datetime.datetime.now(tz).isoformat()
    return timestamp


def get_timestamp(timezone="Asia/Kolkata") -> datetime.datetime:
    tz = pytz.timezone(timezone)
    timestamp = datetime.datetime.now(tz)
    return timestamp


def remove_dir(tmp_dir_name) -> str:
    if tmp_dir_name is not None:
        shutil.rmtree(tmp_dir_name, ignore_errors=True)
        logger.info(f"{tmp_dir_name =} successfully removed")


def calculate_days_between(date1: str, date2: str):
    """

    :param date1:
    :param date2:
    :return:
    """
    if date1 and date1 not in "N/A" and date2 and date2 not in "N/A":
        date1 = datetime.strptime(date1, "%m/%d/%y")
        date2 = datetime.strptime(date2, "%m/%d/%y")
        object = date2 - date1
        return object.days
    else:
        return ""




