from abc import ABC, abstractclassmethod


class CurrentRequestsInterface(ABC):
    @abstractclassmethod
    async def lock(cls, url: str) -> bool: pass

    @abstractclassmethod
    async def unlock(cls, url: str): pass


