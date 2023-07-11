from pydantic import BaseModel, BaseConfig, BaseSettings, PostgresDsn, SecretStr, PositiveInt, Field, RedisDsn, EmailStr

import ujson


class Config(BaseConfig):
    json_dumps = ujson.dumps
    json_loads = ujson.loads
    orm_mode = True


class Schema(BaseModel):
    Config = Config


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn
    SECRET_KEY: SecretStr
    EXPIRE_JWT: PositiveInt
    ALGORITHM: str = Field(default='HS256')
    TOKEN_TYPE: str = Field(default='Bearer')
    SMTP_PASSWORD: SecretStr
    SMTP_PORT: PositiveInt
    SMTP_HOST: str
    SMTP_USER: EmailStr
    # class Config:
    #     env_file = '.env'
