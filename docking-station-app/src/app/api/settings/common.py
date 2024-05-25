from datetime import timedelta
from typing import Annotated, Callable

from fastapi import Request, Response
from pydantic import BeforeValidator
from pytimeparse.timeparse import timeparse

__all__ = [
    'cache_key_builder',
    'Interval',
]


def _validate_interval(value):
    match value:
        case str() if value.isdigit():
            return timedelta(seconds=int(value))
        case str():
            return timedelta(seconds=timeparse(value))
    return value


def cache_key_builder(func: Callable,
                      namespace: str = '',
                      request: Request = None,
                      response: Response = None,
                      args: tuple = None,
                      kwargs: dict = None):
    args = args or ()
    kwargs = kwargs or {}
    args_values = [
        *[f'{a!r}' for a in args],
        *[f'{k}={v!r}' for k, v in kwargs.items()],
    ]
    args_str = ','.join(args_values)

    return f'{func.__module__}.{func.__name__}({args_str})'


Interval = Annotated[timedelta, BeforeValidator(_validate_interval)]
