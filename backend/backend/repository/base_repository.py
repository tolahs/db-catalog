from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Optional
from uuid import uuid4

from sqlalchemy import delete as sql_delete
from sqlalchemy import select
from sqlalchemy import update as sql_update
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import Mapped, mapped_column

from ..config import Base, DatabaseSession


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(primary_key=True, default=None)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    deleted_at: Mapped[datetime] = mapped_column(default=None, nullable=True)
    created_by: Mapped[str]
    updated_by: Mapped[str]
    deleted_by: Mapped[str] = mapped_column(default=None, nullable=True)


class BaseRepository(ABC):

    def __init__(self, db: DatabaseSession, entity: object):
        self.db = db
        self.entity: Any = entity

    @staticmethod
    def set_default_for_create(entity: BaseModel) -> BaseModel:
        entity.id = str(uuid4())
        entity.created_at = datetime.now()
        entity.updated_at = datetime.now()
        entity.created_by = "admin"
        entity.updated_by = "admin"
        return entity

    @staticmethod
    def set_default_for_update(entity: Any) -> Any:
        entity.updated_at = datetime.now()
        entity.updated_by = "admin"
        return entity

    @staticmethod
    def set_default_for_delete(entity: Any) -> Any:
        entity.deleted_at = datetime.now()
        entity.deleted_by = "admin"
        return entity

    @abstractmethod
    async def get_one_by_id(self, id: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def find_one_by(
        self, filter: dict, query_options: Optional[dict] = None
    ) -> Optional[Any]:
        pass

    @abstractmethod
    async def find_all_by(
        self, filter: dict, query_options: Optional[dict] = None
    ) -> List[Any]:
        pass

    @abstractmethod
    async def find_all(self, query_options: Optional[dict] = None) -> List[Any]:
        pass

    @abstractmethod
    async def create_one(self, data: Any, query_options: Optional[dict] = None) -> Any:
        pass

    @abstractmethod
    async def create_many(
        self, data: List[Any], query_options: Optional[dict] = None
    ) -> List[Any]:
        pass

    @abstractmethod
    async def update_one(
        self, id: str, data: dict, query_options: Optional[dict] = None
    ) -> Any:
        pass

    @abstractmethod
    async def delete_one(self, id: str, query_options: Optional[dict] = None) -> int:
        pass

    @abstractmethod
    async def delete_many(
        self, ids: List[str], query_options: Optional[dict] = None
    ) -> int:
        pass

    @abstractmethod
    async def soft_delete_one(
        self, id: str, query_options: Optional[dict] = None
    ) -> int:
        pass

    @abstractmethod
    async def soft_delete_many(
        self, ids: List[str], query_options: Optional[dict] = None
    ) -> int:
        pass


class BasicRepository(BaseRepository):

    async def get_one_by_id(self, id: str) -> Optional[object]:
        async with self.db as session:
            stmt = select(self.entity).where(
                self.entity.id == id, self.entity.deleted_at.is_(None)
            )

            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    async def find_one_by(
        self, filter: dict, query_options: Optional[dict] = None
    ) -> Optional[object]:
        async with self.db.session as session:
            stmt = (
                select(self.entity)
                .filter_by(**filter)
                .where(self.entity.deleted_at.is_(None))
            )  # type: ignore

            if query_options and "order_by" in query_options:
                stmt = stmt.order_by(query_options["order_by"])

            result = await session.execute(stmt)
            return result.scalars().first()

    async def find_all_by(
        self, filter: dict, query_options: Optional[dict] = None
    ) -> List[object]:
        async with self.db.session as session:
            stmt = (
                select(self.entity)
                .filter_by(**filter)
                .where(self.entity.deleted_at.is_(None))
            )  # type: ignore

            if query_options and "order_by" in query_options:
                stmt = stmt.order_by(query_options["order_by"])

            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def find_all(self, query_options: Optional[dict] = None) -> List[object]:
        async with self.db.session as session:
            stmt = select(self.entity).where(self.entity.deleted_at.is_(None))  # type: ignore

            if query_options and "order_by" in query_options:
                stmt = stmt.order_by(query_options["order_by"])
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def create_one(
        self, entity: Any, query_options: Optional[dict] = None
    ) -> Any:
        async with self.db as session:
            async with session.begin():
                entity = self.set_default_for_create(entity)
                session.add(entity)
            await session.commit()
            await session.refresh(entity)
            return entity

    async def create_many(
        self, entities: List[Any], query_options: Optional[dict] = None
    ) -> List[Any]:
        async with self.db.session as session:
            async with session.begin():
                for entity in entities:
                    entity = self.set_default_for_create(entity)

                session.add_all(entities)
            await session.commit()            
            return entities

    async def update_one(
        self, id: str, data: dict, query_options: Optional[dict] = None
    ) -> object:
        async with self.db.session as session:
            stmt = select(self.entity).where(
                self.entity.id == id, self.entity.deleted_at.is_(None)
            )  # type: ignore
            result = await session.execute(stmt)

            entity = result.scalars().one_or_none()
            if not entity:
                raise ValueError(f"Entity with id {id} not found")
            for key, value in data.items():
                setattr(entity, key, value)
            entity = self.set_default_for_update(entity)

            await session.commit()
            await session.refresh(entity)
            return entity

    async def delete_one(self, id: str, query_options: Optional[dict] = None) -> int:
        async with self.db.session as session:
            query = sql_delete(self.entity).where(  # type: ignore
                self.entity.id == id, self.entity.deleted_at.is_(None)
            )  # type: ignore
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def delete_many(
        self, ids: List[str], query_options: Optional[dict] = None
    ) -> int:
        async with self.db.session as session:
            query = sql_delete(self.entity).where(  # type: ignore
                self.entity.id.in_(ids), self.entity.deleted_at.is_(None)
            )  # type: ignore
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def soft_delete_one(
        self, id: str, query_options: Optional[dict] = None
    ) -> int:
        async with self.db.session as session:
            query = sql_update(self.entity).where(  # type: ignore
                self.entity.id == id, self.entity.deleted_at.is_(None)
            ).values(deleted_at=datetime.now(), deleted_by="admin")  # type: ignore
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def soft_delete_many(
        self, ids: List[str], query_options: Optional[dict] = None
    ) -> int:
        async with self.db.session as session:
            query = sql_update(self.entity).where(  # type: ignore
                self.entity.id.in_(ids), self.entity.deleted_at.is_(None)
            ).values(deleted_at=datetime.now(), deleted_by="admin")  # type: ignore
            result = await session.execute(query)
            await session.commit()
            return result.rowcount