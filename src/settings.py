from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    servig_port: int = Field(..., env='SERVING_PORT')
    receive_from: str = Field(..., env='RECEIVE_FROM')
    redirect_to: str = Field(..., env='REDIRECT_TO')
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    class Config:
        env_prefix = ''
        case_sensitive = False