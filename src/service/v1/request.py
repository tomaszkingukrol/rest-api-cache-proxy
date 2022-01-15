import asyncio
import aiohttp
from urllib.parse import urlparse
from fastapi import Request, Response

from settings import Settings
from model.response import ResponseModel
from cache.requests_cache_redis import Cache
from cache.current_requests_redis import CurrentRequests


def url_map(url: str, target_loc: str = Settings().target_location) -> str:
    return urlparse(url)._replace(netloc=target_loc).geturl()


async def get_response(request: Request) -> Response:
    response = await _get_response(request)
    return Response(**response.dict())  


async def _get_response(request: Request) -> Response:
    url = url_map(str(request.url))
    response = await Cache.get(url)
    if not response: 
        if CurrentRequests.lock(url):
            response = await asyncio.create_task(ask_for_response(request))
            response.headers['Cache-Control-Source'] = 'origin'
        else:
            await asyncio.sleep(0.005)
            response = await _get_response(request)
    return response


async def ask_for_response(request: Request) -> Response:
    try:
        url = url_map(str(request.url))
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
                ttl = int(response.headers['Cache-Control-TTL'])
                if ttl:
                    await Cache.set(url, response, int(ttl))
            return response

    except Exception as ex:
        raise ex
    finally:
        CurrentRequests.unlock(url)
