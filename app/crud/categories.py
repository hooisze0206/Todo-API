

from app.models.categories_model import *
from sqlmodel import Session, select, delete
from app.models.categories_model import Categories, CategoriesRead, CategoriesCreate
from sqlalchemy import text

def create_categories(db: Session, db_category: Categories):
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def remove_all_categories(db: Session):
    # Use the session to execute a bulk delete
    statement = delete(Categories)
    categories_crud = db.exec(statement)

    print(categories_crud)
    #
    db.commit()
    print("All categories removed successfully.")
    return True

def get_total_task_categories(db: Session):
    query = text("SELECT * FROM vw_total_categories_of_task")
    result = db.exec(query)
    categories = result.fetchall()

    return categories