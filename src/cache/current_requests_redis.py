import redis 

from settings import Settings
from cache.current_requests_abstract import CurrentRequestsInterface


class CurrentRequests(CurrentRequestsInterface):
    _cache = redis.Redis(
        host=Settings().redis_host,
        port=Settings().redis_port,
        db=1)
    _cache.flushdb()

    @classmethod
    def lock(cls, url: str) -> bool:
        res = cls._cache.set(url, 1, nx=True)
        return res

    @classmethod
    def unlock(cls, url: str):
        cls._cache.delete(url)


