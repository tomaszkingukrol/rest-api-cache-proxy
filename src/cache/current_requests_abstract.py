from abc import ABC, abstractclassmethod


class CurrentRequestsInterface(ABC):
    @abstractclassmethod
    async def check(cls, url: str) -> bool: pass

    @abstractclassmethod
    def set(cls, url: str): pass

    @abstractclassmethod
    def delete(cls, url: str): pass


