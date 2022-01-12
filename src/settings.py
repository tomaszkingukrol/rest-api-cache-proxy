from pydantic import BaseSettings, BaseConfig


class Settings(BaseSettings):
    servig_port: int
    receive_from: str
    redirect_to: str
    redis_host: str
    redis_port: int

    class Config:
        env_file = 'racp.env'
        env_file_encoding = 'utf-8'