import asyncio
import aiohttp
from fastapi import Request, Response

from model.response import ResponseModel
from cache.requests_cache_redis import Cache
from cache.current_requests_redis import CurrentRequests


mapping = {'source': None, 'destination': None}


async def get_response(request: Request) -> Response:
    response = await Cache.get(str(request.url))
    if not response: 
        if not await CurrentRequests.check(str(request.url)):
            CurrentRequests.set(str(str(request.url)))
            response = await asyncio.create_task(ask_for_response(request))
            response.headers['Cache-Control-Source'] = 'origin'
        else:
            while not response:
                await asyncio.sleep(0.005)
                response = await Cache.get(str(request.url))
    return Response(**response.dict())  


async def ask_for_response(request: Request) -> Response:
    try:
        url = str(request.url).replace(mapping['source'], mapping['destination'])

        conn = aiohttp.TCPConnector(ssl=False)
        headers = request.headers
        async with aiohttp.ClientSession(connector=conn, headers=headers) as session:

            resp = await session.get(url)
            content = await resp.text()

            response = ResponseModel(
                content=content,
                status_code=resp.status,
                headers=resp.headers,
                media_type=resp.content_type
            )

            if 'Cache-Control-TTL' in response.headers:
                ttl = response.headers['Cache-Control-TTL']
                await Cache.set(str(request.url), response, int(ttl))
                
            return response

    except Exception as ex:
        raise ex
    finally:
        CurrentRequests.delete(str(request.url))
