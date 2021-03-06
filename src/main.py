import fastapi
import uvicorn
import logging

from settings import Settings
from api.v1 import request, healthcheck

v1 = fastapi.APIRouter()
v1.include_router(healthcheck.v1)
v1.include_router(request.v1)

api = fastapi.FastAPI(
    title="REST api cache proxy",
    version="0.0.1"    
)
api.include_router(v1)

@api.exception_handler(Exception)
async def unicorn_exception_handler(request: fastapi.Request, ex: Exception):
    logging.getLogger('uvicorn.default').error(f'{ex}')
    return fastapi.responses.JSONResponse(
        status_code=500,
        content={"message": f"Oops! something went wrong"},
    )

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s %(levelname)s %(message)s"    
    uvicorn.run("main:api", host=Settings().servig_host, port=Settings().servig_port, log_config=log_config, reload=True)


