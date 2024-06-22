import os
import logging  # Import logging module
from typing import Any

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import JSON
from sqlalchemy import text

# Configure logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

load_dotenv(verbose=True)

DB_CONFIG: str = os.environ["DB_CONFIG"]
if not DB_CONFIG:
    raise EnvironmentError("The environment variable 'DB_CONFIG' is not set.")



class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}


class DatabaseSession:

    def __init__(self, url: str = DB_CONFIG):
        self.db_url = url
        self.engine: AsyncEngine = create_async_engine(url, echo=True)  # Enable echo
        self.SessionLocal = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )   
    async def create_db_if_not_exists(self):
        # Extract the database name from the URL
        
        db_name = self.db_url.rsplit('/', 1)[-1]
        default_db_url = self.db_url.rsplit('/', 1)[0] + '/postgres'

        # Connect to the default 'postgres' database
        default_engine = create_async_engine(default_db_url, echo=True)
        async with default_engine.connect() as conn:
            result = await conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            )
            exists = result.scalar() is not None

            if not exists:
                await conn.execute(text(f"COMMIT"))  # Ensure no transaction is active
                await conn.execute(text(f"CREATE DATABASE {db_name}"))

        await default_engine.dispose()

    async def create_all(self):
        await self.create_db_if_not_exists()
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    # Closing the database connection
    async def close(self):
        await self.engine.dispose()

    # Prepare context for the async operations
    async def __aenter__(self) -> AsyncSession:
        self.session = self.SessionLocal()
        return self.session

    # it is used to clean up resource , etc.
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close_all()

    async def commit_rollback(self):
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

db: DatabaseSession = DatabaseSession()
