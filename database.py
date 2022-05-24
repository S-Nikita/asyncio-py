import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    )
from sqlalchemy import (
    Column,
    Integer,
    String,
)


Base = declarative_base()

class SW_Character(Base):
    __tablename__ = 'sw_characters'
    row_id = Column(Integer, primary_key = True)
    id = Column(Integer)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)


async def db_main(data):
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:756894@localhost:5432/star_wars",
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        async with session.begin():
            for item in data:
                char = SW_Character(
                                        id = item['id'],
                                        birth_year = item['birth_year'],
                                        eye_color = item['eye_color'],
                                        films = item['films'],
                                        gender = item['gender'],
                                        hair_color = item['hair_color'],
                                        height = item['height'],
                                        homeworld = item['homeworld'],
                                        mass = item['mass'],
                                        name = item['name'],
                                        skin_color = item['skin_color'],
                                        species = item['species'],
                                        starships = item['starships'],
                                        vehicles = item['vehicles']
                                    )
                session.add(char)
                await session.commit()

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())