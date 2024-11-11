from functools import wraps
from typing import get_type_hints

def convert_result(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        return_type = get_type_hints(func).get("return", None)
        if return_type and not isinstance(result, return_type):
            result = return_type(**result)
        return result
    return async_wrapper
