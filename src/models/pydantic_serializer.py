

# -*- coding: utf-8 -*-
"""

@Filename : pydantic serializer
@created :  Dec 7 11:42 2020
@project: lambda-exchange-tracker
@author : Nikkhil Butola
"""

import typing
import uuid

from pydantic import BaseModel, field_validator, EmailStr, Field, validator
from datetime import timedelta, date, time, datetime
from src import constants

__all__ = ["EventScrapeData", "CurrencyExchangeModel", "CurrencyExchange"]


class CurrencyExchange(BaseModel):
    index: str
    symbol: str
    currency: str
    spot_rate: str
    fluctuation: typing.Union[str, float]

    class Config:
        from_attributes = True

    @field_validator("fluctuation")
    def convert_fluctuation(cls, fluctuation):
        return str(fluctuation) if isinstance(fluctuation, float) else fluctuation


class CurrencyExchangeModel(BaseModel):
    metadata: typing.List[CurrencyExchange]


class EventScrapeData(BaseModel):
    event_id: str
    user_id: typing.Optional[str] = ""
    website_uri: typing.Optional[str] = ""

    class Config:
        from_attributes = True
        validate_assignment = True

    @field_validator("website_uri")
    def set_website_uri(cls, website_uri):
        return website_uri or constants.scrape_website_uri