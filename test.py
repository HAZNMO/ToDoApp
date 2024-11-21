from pydantic import BaseModel

from to_do_app.API.utils.decorator_convert import convert_result


class A(BaseModel):
    a:int
    b:str


@convert_result
async def main() -> list[A]:
    return [{"a":1, "b":"2"},{"a":1, "b":"2"}]



async def run():
    result = await main()
    from devtools import debug

    debug(result)
if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
