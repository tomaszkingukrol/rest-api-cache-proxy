from fastapi import APIRouter, Response
from fastapi.responses import HTMLResponse
import logging

from service.v1.healthcheck import get_healthcheck


v1 = APIRouter()


@v1.get('/rest-api-cache-proxy/healthcheck', response_class=HTMLResponse)
async def healthcheck():
    return await get_healthcheck()


