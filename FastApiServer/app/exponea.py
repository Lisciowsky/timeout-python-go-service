# Python Standard
from typing import Union, Literal
from datetime import datetime
from time import sleep
from threading import Thread
import json
import asyncio
from enum import Enum

# Third Party
import requests_async as requests

# Local
import settings
import models
from utils import log_message, ThreadWithReturnValue

# request results placeholder
data = {}


class RequestsEnum(Enum):
    First = "First"
    Second = "Second"
    Third = "Third"


async def get_responses_async(timeout: int):
    messages = list()
    first_request = asyncio.create_task(
        get_response_from_exponea(data, RequestsEnum.First, status_code=400)
    )
    start = get_time_in_milisecond()
    await first_request

    while get_time_in_milisecond() - start < 300:
        if data[RequestsEnum.First.value] == settings.STATUS_CODE_200:
            log_message(
                "SUCCESS: first request managed within 300 ms and returned 200 status code !"
            )
            return models.ExponeaSuccessReponse(timeout=timeout)

        elif data[RequestsEnum.First.value] != settings.STATUS_CODE_200:
            log_message(
                f"First request was able to return within 300 ms but status code is {data[RequestsEnum.First.value]}!"
            )
            break

    await asyncio.gather(
        get_response_from_exponea(data, RequestsEnum.Second, status_code=400),
        get_response_from_exponea(data, RequestsEnum.Third, status_code=200),
    )

    for request_num in list(RequestsEnum.__members__):
        result = data.get(request_num)
        if result is not None:
            if result == settings.STATUS_CODE_200:
                log_message(f"SUCCESS: Found correct response in {request_num}")
                return models.ExponeaSuccessReponse(timeout=timeout)

        if request_num == list(RequestsEnum.__members__)[-1]:
            message = "All three requests returned wrong response code."
            log_message(message=message, level="WARNING")
            return models.ExponeaErrorResponse(message="WARNING: " + message)


async def get_response_from_exponea(
    data, request_num: RequestsEnum, status_code: int = 400
):
    response = await requests.get(url=settings.EXPONEA_URL)
    data[request_num.value] = response.status_code


# async def get_response_from_exponea(
#     data, request_num: RequestsEnum, status_code: int = 400
# ):
#     log_message("Sleeping for 1 second")
#     await asyncio.sleep(0.05)
#     log_message("Sleeping finished...")
#     data[request_num.value] = status_code


def get_time_in_milisecond() -> int:
    """returns timestamp in miliseconds"""
    return int(datetime.now().timestamp()) * 1000


def _get_decorator(timeout: int):
    return decorator_factory(timeout=timeout)


async def entrypoint(
    timeout: int,
) -> Union[models.ExponeaErrorResponse, models.ExponeaSuccessReponse]:
    """
    Function responsible for calling Exponea Server, with requested timeout from client.
    """
    future = get_responses_async(timeout=timeout)
    try:
        response = await asyncio.wait_for(fut=future, timeout=(timeout / 1000))
        return response
    except asyncio.TimeoutError:
        return models.ExponeaErrorResponse(message=f"Timeout: {timeout}")
