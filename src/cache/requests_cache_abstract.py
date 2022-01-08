from abc import ABC, abstractclassmethod
from fastapi import Response


class CacheInterface(ABC):
    @abstractclassmethod
    async def get(cls, url: str) -> Response: pass

    @abstractclassmethod
    async def set(cls, url: str, value: Response, ttl=0): pass

