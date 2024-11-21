from collections.abc import Callable
from functools import wraps
from typing import get_type_hints

from pydantic import TypeAdapter


def convert_result(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return_type = get_type_hints(func).get("return", None)

        if not return_type:
            raise Exception(f"No return type for  {func.__name__}")


        result = await func(*args, **kwargs)
        items = TypeAdapter(return_type).validate_python(result)


        return items
    return wrapper
