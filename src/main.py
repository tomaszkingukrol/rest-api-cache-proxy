import fastapi
import uvicorn
import argparse
import os

from api.v1 import request, healthcheck
from service.v1.request import mapping


parser = argparse.ArgumentParser(description='REST api cache proxy')
parser.add_argument('--host', type=str, help='REST api cache proxy host')
parser.add_argument('--port', type=int, help='REST api cache proxy port')
args = parser.parse_args()


mapping['source'] = args.host
mapping['destination'] = '127.0.0.100'


v1 = fastapi.APIRouter()
v1.include_router(healthcheck.v1)
v1.include_router(request.v1)


api = fastapi.FastAPI(
    title="REST api cache proxy",
    version="0.0.1"    
)
api.include_router(v1)


if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s %(levelname)s %(message)s"    
    uvicorn.run("main:api", host=args.host, port=args.port, log_config=log_config, reload=True)


