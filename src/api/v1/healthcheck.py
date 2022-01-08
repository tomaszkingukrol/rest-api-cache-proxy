from fastapi import APIRouter, Response
from fastapi.responses import HTMLResponse
import logging

from service.v1.healthcheck import get_healthcheck


v1 = APIRouter()


@v1.get('/rest-api-cache-proxy/healthcheck', response_class=HTMLResponse)
async def healthcheck():
    try:
        response = await get_healthcheck()
    except Exception as ex:
        logging.getLogger('uvicorn.default').error('Error during healthcheck {ex}')
        return Response(content='REST api cache proxy internal error', status_code=500)       
    else:
        return response  


