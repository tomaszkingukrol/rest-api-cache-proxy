import redis 
import os

from cache.current_requests_abstract import CurrentRequestsInterface


class CurrentRequests(CurrentRequestsInterface):
    _cache = redis.Redis(
        host=os.getenv("RACP-redis-host", "127.0.0.1"),
        port=os.getenv("RACP-redis-port", 6379),
        db=1)
    _ttl_ms = os.getenv("RACP-redis-current-requests-ttl-ms", 50)

    @classmethod
    async def check(cls, url: str) -> bool:
        res = cls._cache.get(url)
        return res and bool(res)

    @classmethod
    def set(cls, url: str):
        cls._cache.psetex(url, cls._ttl_ms, 'None')   

    @classmethod
    def delete(cls, url: str):
        cls._cache.delete(url)

