from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    servig_host: str = Field(..., env='SERVING_HOST')
    servig_port: int = Field(..., env='SERVING_PORT')
    target_location: str = Field(..., env='TARGET_LOCATION')
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    class Config:
        env_prefix = ''
        case_sensitive = False