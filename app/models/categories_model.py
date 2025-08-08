from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
import uuid

def generate_uuid():
    """Generate a unique UUID for a task."""
    return str(uuid.uuid4())

class CategoriesBase(SQLModel):
    """Base model for task data."""
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    color: str = Field(default=None)

class Categories(CategoriesBase, table=True):
    """Database model for tasks."""
    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        index=True
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

class CategoriesRead(CategoriesBase):
    """Model for reading a task."""
    id: str
    created_at: datetime
    updated_at: datetime

class CategoriesCreate(CategoriesBase):
    """Model for creating a new task."""
    pass

    