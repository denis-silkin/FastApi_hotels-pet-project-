import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


engine = create_async_engine(settings.DB_URL)


# async def func():
#     async with engine.begin() as conn:
#         res = await conn.execute(text("SELECT version()"))
#         print(res.fetchone())
#
# asyncio.run(func())

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

# session = async_session_maker()
# await session.execute()


class Base(DeclarativeBase):
    pass
