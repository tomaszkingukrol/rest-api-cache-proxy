from fastapi import APIRouter, Request, Response
import logging

from service.v1.request import get_response


v1 = APIRouter()


@v1.get('/{any:path}', response_class=Response)
async def get_request(request: Request, any: str):
    return await get_response(request)
