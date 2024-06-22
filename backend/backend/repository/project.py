from typing import Any, Optional

from sqlalchemy.orm import Mapped, mapped_column

from .base_repository import BaseModel, BasicRepository


class Project(BaseModel):  # type: ignore

    __tablename__ = "project"  # type: ignore

    # Project datasource type. ex: bigquery, mysql, postgresql, mongodb, etc
    type: Mapped[str] = mapped_column(nullable=False)

    display_name: Mapped[str] = mapped_column(nullable=False)

    catalog: Mapped[str]

    schema: Mapped[str]

    connection_info: Mapped[Optional[dict[str, Any]]]  # Connection info


class ProjectRepository(BasicRepository): ...
