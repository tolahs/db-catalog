from typing import Any, List, Optional

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model_column import ModelColumn
from backend.repository.base_repository import BasicRepository

from .project import Project


class Model(SQLModel, table=True):  # type: ignore
    
    __tablename__ = "model"  # type: ignore

    # Reference to project.id
    project_id: Mapped[str] = mapped_column(ForeignKey(f"{Project.__tablename__}.id"))

    # Model name displayed in UI
    display_name: Mapped[str] = mapped_column(nullable=False)

    # The table name in the datasource
    source_table_name: Mapped[str] = mapped_column(nullable=False)

    # The name used in the MDL structure
    reference_name: Mapped[str] = mapped_column(nullable=False)

    # Reference SQL
    ref_sql: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)

    # Model is cached or not
    cached: Mapped[Optional[bool]]

    # Contain a number followed by a time unit (ns, us, ms, s, m, h, d). For example, "2h"
    refresh_time: Mapped[Optional[str]]

    # Model properties, a json string, the description and displayName should be stored here
    properties: Mapped[Optional[dict[str, Any]]] 

    Columns: Mapped[List[ModelColumn]] = relationship(back_populates=f"{ModelColumn.__tablename__}_parent_{__tablename__}")

class ModelRepository(BasicRepository):
    ...