from typing import Any, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .project import Project
from .base_repository import BaseModel, BasicRepository


class ColumnRelation(BaseModel):  # type: ignore
    
    __tablename__ = "relation" 
    
    
    project_id: Mapped[str] = mapped_column(ForeignKey(f"{Project.__tablename__}.id"))
    
    # Relation name
    name: Mapped[str] = mapped_column(nullable=False)  
    
    # Join type, eg:"MANY_TO_ONE", "ONE_TO_MANY", "MANY_TO_MANY"
    join_type: Mapped[str] = mapped_column(nullable=False)  
    
    # Join condition, ex: "OrdersModel.custkey = CustomerModel.custkey"
    condition: Mapped[str] = mapped_column(nullable=False)  
    
    
    # from column id, "{fromColumn} {joinType} {toColumn}"
    from_column_id: Mapped[int] = mapped_column(nullable=False)  
    
    # to column id, "{fromColumn} {joinType} {toColumn}"
    to_column_id: Mapped[int] = mapped_column(nullable=False)  
    
    # Model properties, a json string, the description should be stored here
    properties: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)  

class ExtraRelationInfo(BaseModel):
    from_model_id: Mapped[int] = mapped_column(nullable=False)
    from_model_name: Mapped[str] = mapped_column(nullable=False)
    from_model_display_name: Mapped[str] = mapped_column(nullable=False)
    from_column_name: Mapped[str] = mapped_column(nullable=False)
    from_column_display_name: Mapped[str] = mapped_column(nullable=False)
    to_model_id: Mapped[int] = mapped_column(nullable=False)
    to_model_name: Mapped[str] = mapped_column(nullable=False)
    to_model_display_name: Mapped[str] = mapped_column(nullable=False)
    to_column_name: Mapped[str] = mapped_column(nullable=False)
    to_column_display_name: Mapped[str] = mapped_column(nullable=False)

class ColumnRelationInfo(ColumnRelation, ExtraRelationInfo):
    ...
class ColumnRelationRepository(BasicRepository):
    ...