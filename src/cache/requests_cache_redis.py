import aioredis 
import json
import os

from model.response import ResponseModel
from cache.requests_cache_abstract import CacheInterface


class Cache(CacheInterface):
    _cache = aioredis.Redis(
        host=os.getenv("RACP-redis-host", "127.0.0.1"),
        port=os.getenv("RACP-redis-host", 6379),
        db=0)

    @classmethod
    async def get(cls, url: str) -> ResponseModel:
        data = await cls._cache.get(url)
        return data and ResponseModel(**json.loads(data))

    @classmethod
    async def set(cls, url: str, data: ResponseModel, ttl=0):
        data.headers['Cache-Control-Source'] = 'cached'
        await cls._cache.setex(url, ttl, json.dumps(data.dict()))


