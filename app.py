import time
import asyncio

from helpers import Cache
from datetime import timedelta, datetime


class MyCache(Cache):
    __memory = dict()

    def set(self, key: str, value: str, ttl: timedelta):
        value = {"value": value, "ttl": ttl, "time": datetime.now()}
        self.__memory[key] = value

    def get(self, key: str) -> str | None:
        m = self.__memory.get(key, {})
        if m:
            td = datetime.now() - m["time"]
            if m["ttl"] >= td:
                return m["value"]

        return None

    def clean_up(self) -> None:
        for key, value in self.__memory.copy().items():
            td = datetime.now() - value["time"]
            if value["ttl"] < td:
                del self.__memory[key]


# corutine
async def update_cache(cache: Cache):
    cache.set("key1", "value1", timedelta(seconds=3))
    print(cache.get("key1"))  # Should return 'value1'
    print(cache.get("key2"))  # Should return None (since "key2" is not in the cache)

    # After 3 seconds
    time.sleep(5)
    print(cache.get("key1"))  # Should return None (because the key expired)


# corutine
async def clean_up(cache: Cache):
    while True:
        cache.clean_up()
        await asyncio.sleep(1)


# event loop
async def main():
    task1 = asyncio.create_task(update_cache())
    task2 = asyncio.create_task(clean_up())

    await task1
    await task2


async def main():
    cache = MyCache()
    task1 = asyncio.create_task(update_cache(cache))
    task2 = asyncio.create_task(clean_up(cache))

    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())
