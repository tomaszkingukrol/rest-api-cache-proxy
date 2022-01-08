from fastapi import APIRouter, Request, Response
import pydantic
import logging

from service.v1.request import get_response


v1 = APIRouter()


@v1.get('/{any:path}', response_class=Response)
async def request(request: Request, any: str):
    try:
        response = await get_response(request)
    except Exception as ex:
        logging.getLogger('uvicorn.default').error(f'Error during request responding {ex}')
        return Response(content=f'REST api cache proxy internal error {ex}', status_code=500)       
    else:
        return response  


