from typing import Any, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.repository.project import Project
from .base_repository import BaseModel, BasicRepository


class View(SQLModel, table=True):  # type: ignore
    
    __tablename__ = "view"  # type: ignore

    
    project_id: Mapped[str] = mapped_column(ForeignKey(f"{Project.__tablename__}.id"))
    
    # The view name
    name: Mapped[str] = mapped_column(nullable=False)  
    
    # The SQL statement of this view
    statement: Mapped[str] = mapped_column(nullable=False)  
    
    cached: Mapped[bool] = mapped_column(nullable=False)  # View is cached or not
    
    # Contain a number followed by a time unit (ns, us, ms, s, m, h, d). For example, "2h"
    refresh_time: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)
    
    # View properties, a json string, the description and displayName should be stored here
    properties: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)
    
    

class ViewRepository(BasicRepository):
    ... 