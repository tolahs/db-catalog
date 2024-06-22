from typing import Any, List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_repository import BaseModel, BasicRepository
from .model import Model
from .model_column import ModelColumn
from .view import View

class Project(BaseModel):  # type: ignore
    
    __tablename__ = "project"  # type: ignore
    
    # Project datasource type. ex: bigquery, mysql, postgresql, mongodb, etc
    type: Mapped[str] = mapped_column(nullable=False)
    
    display_name: Mapped[str] = mapped_column(nullable=False)
    
    catalog: Mapped[str]
    
    schema: Mapped[str]
    
    connection_info: Mapped[Optional[dict[str, Any]]]  # Connection info

    Models: Mapped[List[Model]] = relationship(back_populates=f"{Model.__tablename__}_parent_{__tablename__}")

    Views: Mapped[List[View]] = relationship(back_populates=f"{View.__tablename__}_parent_{__tablename__}")

class ProjectRepository(BasicRepository):
    ...
