from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database.config import get_session
from app.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from app.crud import task as task_crud

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(*, session: Session = Depends(get_session), task: TaskCreate):
    """
    Create a new task.

    - **title**: Required. The title of the task.
    - **description**: Optional. Detailed description of the task.
    - **priority**: Optional. Priority level (1-5), defaults to 1.
    - **completed**: Optional. Task completion status, defaults to False.
    - **subTasks**: Optional. SubTasks, defaults to empty.
    """
    # Convert TaskCreate model to Task model
    db_task = Task.from_orm(task)
    print(f"Creating task: {db_task}")

    # Add to database
    task_crud.create_task(session, db_task)

    return db_task

@router.get("/", response_model=List[TaskRead])
def read_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100,
    completed: bool = None
):
    """
    Retrieve a list of tasks with optional filtering.

    - **offset**: Number of tasks to skip (for pagination).
    - **limit**: Maximum number of tasks to return (for pagination).
    - **completed**: Filter by completion status.
    """
    query = select(Task)

    # Apply completion status filter if provided
    if completed is not None:
        query = query.where(Task.completed == completed)

    # Apply pagination
    tasks = session.exec(query.offset(offset).limit(limit)).all()
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
def read_task(*, session: Session = Depends(get_session), task_id: str):
    """
    Retrieve a specific task by ID.

    - **task_id**: The unique identifier of the task.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task

...
@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    *,
    session: Session = Depends(get_session),
    task_id: str,
    task: TaskUpdate
):
    """
    Update a task completely.

    - **task_id**: The unique identifier of the task.
    - Request body: All task fields (even unchanged ones).
    """
    print(task)
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    # Update all attributes
    db_task = task_crud.update_task(session, db_task, task)

    return db_task


...
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(*, session: Session = Depends(get_session), task_id: str):
    """
    Delete a task.

    - **task_id**: The unique identifier of the task.
    """

    isRemoved = task_crud.remove_task(session, task_id)
    if not isRemoved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    # Return no content
    return None
    
...
@router.delete("/remove_all", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_task(*, session: Session = Depends(get_session)):
    """
    Delete all task.
    """

    isRemoved = task_crud.remove_all_task(session)
    if not isRemoved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found"
        )

    # Return no content
    return None
