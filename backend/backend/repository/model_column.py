from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_repository import BaseModel


class ModelColumn(BaseModel):

    __tablename__ = "model_column"  # type: ignore

    model_id: Mapped[str] = mapped_column(ForeignKey(f"model.id"))

    is_calculated: Mapped[bool] = mapped_column(nullable=False)  # Is calculated field

    display_name: Mapped[str] = mapped_column(
        nullable=False
    )  # Column name displayed in UI

    # The name used in the MDL structure and when querying the data
    reference_name: Mapped[str] = mapped_column(nullable=False)

    # The column name in the datasource
    source_column_name: Mapped[str] = mapped_column(nullable=False)

    # Expression for the column, could be custom field or calculated field expression
    aggregation: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)

    # The selected field in calculated field, array of ids
    lineage: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)

    # For custom field or custom expression of calculated field
    custom_expression: Mapped[Optional[str]] = mapped_column(
        nullable=True, default=None
    )

    # Data type, refer to the column type in the datasource
    type: Mapped[str] = mapped_column(nullable=False)

    not_null: Mapped[bool] = mapped_column(nullable=False)  # Is not null

    is_pk: Mapped[bool] = mapped_column(nullable=False)  # Is primary key of the table

    # Column properties, a json string, the description and displayName should be stored here
    properties: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)
