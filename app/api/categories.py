from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, asc, desc
from typing import List

from app.database.config import get_session
from app.models.response_model import ResponseModel
from app.models.categories_model import Categories, CategoriesRead, CategoriesCreate
from app.crud import categories as categories_crud

router = APIRouter(prefix="/api/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoriesRead])
def read_categories(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 100
):
    """
    Retrieve a list of tasks with optional filtering.

    - **offset**: Number of tasks to skip (for pagination).
    - **limit**: Maximum number of tasks to return (for pagination).
    - **completed**: Filter by completion status.
    """
    query = select(Categories)

    # Apply completion status filter if provided
    query = query.order_by(desc(Categories.created_at))

    # Apply pagination
    categories = session.exec(query.offset(offset).limit(limit)).all()
    return categories


@router.post("/", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
def create_categories(*, session: Session = Depends(get_session), categories: CategoriesCreate):
    """
    Create a new task.

    - **title**: Required. The title of the task.
    - **description**: Optional. Detailed description of the task.
    - **priority**: Optional. Priority level (1-5), defaults to 1.
    - **completed**: Optional. Task completion status, defaults to False.
    - **subTasks**: Optional. SubTasks, defaults to empty.
    """
    # Convert TaskCreate model to Task model
    db_category = Categories.from_orm(categories)
    print(f"Creating categories: {db_category}")


    # Add to database
    categories = categories_crud.create_categories(session, db_category)

    if not categories:
        raise HTTPException(status_code=404, detail="Fail to add category")

    return {"status": 'success', "detail": categories}


@router.delete("/remove_all",status_code=status.HTTP_204_NO_CONTENT)
def delete_all_categories(*, session: Session = Depends(get_session)):
    """
    Delete all task.
    """

    is_removed = categories_crud.remove_all_categories(session)
    if not is_removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category not found"
        )

    # Return no content
    return None