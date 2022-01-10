from abc import ABC, abstractclassmethod

from model.response import ResponseModel


class CacheInterface(ABC):
    @abstractclassmethod
    async def get(cls, url: str) -> ResponseModel: pass

    @abstractclassmethod
    async def set(cls, url: str, value: ResponseModel, ttl=0): pass

