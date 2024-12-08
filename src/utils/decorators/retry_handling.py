

# -*- coding: utf-8 -*-
"""
@Filename : retry decorator
@created :  Dec 7 11:42 2020
@project: tokenizer token_stream app
@author : Nikkhil Butola
"""

import time
from functools import wraps
import logging
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
loggingFormat = "[%(filename)s: %(lineno)s- %(funcName)11s() ] %(asctime)s: %(name)s:%(levelname)s %(message)s"
logging.basicConfig(format=loggingFormat)

"""
example for marking-up the usage
@perform_retry(max_retries=5, wait_time=1)
def example_function():
    # function that may raise an exception
    pass

"""


def perform_retry(max_retries: int, wait_time: int):
    """

    :param max_retries: number of maximum retries before exist
    :param wait_time: waitin' timelapse in seconds
    :return:
    """

    def _retry_handling(func):
        """

        :param func:
        :return:
        """

        @wraps(func)
        def _wrapper(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """

            retries = 0
            if retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result

                except Exception as e:
                    logger.error(traceback.format_exc())
                    retries += 1
                    time.sleep(wait_time)

            else:
                raise Exception(f"Max retries of function {func} exceeded")

        return _wrapper

    return _retry_handling