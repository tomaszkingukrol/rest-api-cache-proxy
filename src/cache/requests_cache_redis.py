import aioredis 
import json
import logging

from settings import Settings
from model.response import ResponseModel
from cache.requests_cache_abstract import CacheInterface


class Cache(CacheInterface):
    _cache = aioredis.Redis(
        host=Settings().redis_host,
        port=Settings().redis_port,
        db=0)

    @classmethod
    async def get(cls, url: str) -> ResponseModel:
        data = await cls._cache.get(url)
        return data and ResponseModel(**json.loads(data))

    @classmethod
    async def set(cls, url: str, data: ResponseModel, ttl=0):
        data.headers['Cache-Control-Source'] = 'cached'
        await cls._cache.setex(url, ttl, json.dumps(data.dict()))
        logging.getLogger('uvicorn.default').info(f'response for {url} cached for {ttl} sec')

    @classmethod
    async def purge(cls, url: str) -> ResponseModel:
        data = await cls._cache.delete(url)

