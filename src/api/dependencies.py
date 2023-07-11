from datetime import datetime, timedelta

from fastapi import Header, HTTPException
from jose import jwt, JWTError
from sqlalchemy import select
from starlette import status

from src.models import User
from src.schemas import UserFullSchema
from src.settings import SETTINGS


def create_token(sub: str) -> str:
    payload = {
        'sub': sub,
        'exp': datetime.utcnow() + timedelta(seconds=SETTINGS.EXPIRE_JWT)
    }
    return jwt.encode(payload, SETTINGS.SECRET_KEY.get_secret_value(), SETTINGS.ALGORITHM)


async def auth(authorization: str = Header(...)) -> User:
    if not authorization.startswith(SETTINGS.TOKEN_TYPE):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token type')
    authorization = authorization.replace(f'{SETTINGS.TOKEN_TYPE} ', '')
    try:
        payload = jwt.decode(
            token=authorization,
            key=SETTINGS.SECRET_KEY.get_secret_value(),
            algorithms=[SETTINGS.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid token')
    else:
        async with User.async_session() as session:
            user = await session.scalar(
                select(User)
                .filter_by(email=payload.get('sub'))
            )
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found or blocked')
            # print(UserFullSchema.from_orm(user))
            return user
