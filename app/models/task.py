from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
import uuid




def generate_uuid():
    """Generate a unique UUID for a task."""
    return str(uuid.uuid4())


class SubTask(SQLModel, table=True):
    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        index=True
    )
    name: str
    completed: bool = Field(default=False)
    task_id: str = Field(foreign_key="task.id")

    task: Optional["Task"] = Relationship(back_populates="subTasks")

class TaskBase(SQLModel):
    """Base model for task data."""
    title: str = Field(index=True)
    categories: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    priority: int = Field(default=1, ge=1, le=5)
    completed: bool = Field(default=False)
   


class Task(TaskBase, table=True):
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
    subTasks: List[SubTask] = Relationship(back_populates="task")


class TaskCreate(TaskBase):
    """Model for creating a new task."""
    pass


class TaskRead(TaskBase):
    """Model for reading a task."""
    id: str
    created_at: datetime
    updated_at: datetime
    subTasks: List[SubTask]


class TaskUpdate(SQLModel):
    """Model for updating a task."""
    title: Optional[str] = None
    categories: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None
    subTasks: Optional[List[SubTask]] = None
