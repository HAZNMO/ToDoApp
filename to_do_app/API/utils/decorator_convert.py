from functools import wraps
from typing import get_args
from typing import get_origin
from typing import get_type_hints


def convert_result(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        return_type = get_type_hints(func).get("return", None)

        if return_type is None:
            return result

        if not isinstance(return_type, (type, tuple)):
            return result

        origin = get_origin(return_type)
        args = get_args(return_type)

        if origin is list and args:
            inner_type = args[0]
            if isinstance(result, list):
                return [inner_type(**item) if isinstance(item, dict) else item for item in result]

        if return_type and not isinstance(result, return_type):
            if isinstance(return_type, type):
                try:
                    result = return_type(**result)
                except TypeError:
                    return result

        return result
    return wrapper
