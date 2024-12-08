
# -*- coding: utf-8 -*-
"""

@Filename : databases utility helper
@created :  Dec 7 11:42 2020
@project: lambda-exchange-tracker
@author : Nikkhil Butola
"""

import json
from decimal import Decimal
from typing import Any, Callable, Type, TypeVar

from pydantic import BaseModel

ReturnModel = TypeVar("ReturnModel")


class DynamoDBBase(BaseModel):
    pk: str
    sk: str


def wrap_model(
    model: Type[ReturnModel],
) -> Callable[[Callable[..., Any]], Callable[..., ReturnModel]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., ReturnModel]:
        def wrapper(*args, **kwargs) -> ReturnModel:
            res = func(*args, **kwargs)
            return model(**res)  # type: ignore[call-arg]

        return wrapper

    return decorator


def handle_decimals(body):
    return json.loads(json.dumps(body), parse_float=Decimal)
