from inspect import iscoroutinefunction
from typing import Type, Any

from sqlalchemy import Column, INT, create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declared_attr

from .settings import SETTINGS


class Base(DeclarativeBase):
    id = Column(INT, primary_key=True)

    engine = create_engine(SETTINGS.DATABASE_URL)
    session = sessionmaker(bind=engine)

    _async_engine = create_async_engine(
        SETTINGS.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
    )
    async_session = async_sessionmaker(bind=_async_engine)

    @declared_attr
    def __tablename__(cls):
        return ''.join(f'_{i.lower()}' if i.isupper() else i for i in cls.__name__).strip('_')

    @staticmethod
    def create_session(func):
        async def async_wrapper(*args, **kwargs):
            async with Base.async_session() as session:
                return await func(*args, **kwargs, session=session)

        def sync_wrapper(*args, **kwargs):
            with Base.session() as session:
                return func(*args, **kwargs, session=session)

        return async_wrapper if iscoroutinefunction(func) else sync_wrapper

    @create_session
    async def save(self, session: AsyncSession = None) -> None:
        session.add(self)
        await session.commit()
        await session.refresh(self)

    @classmethod
    @create_session
    async def get(cls, pk: Any, session: AsyncSession = None) -> Type["Base"]:
        return await session.get(cls, pk)

    @create_session
    async def delete(self, session: AsyncSession = None) -> None:
        await session.delete(self)
        await session.commit()

    @classmethod
    @create_session
    async def select(cls, sql: Any, session: AsyncSession = None):
        objs = await session.scalars(sql)
        return objs.all()
