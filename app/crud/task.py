from app.models.task import Task, SubTask, TaskCreate, TaskRead, TaskUpdate
from sqlmodel import Session, select


def create_task(db: Session, db_task: Task):
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, db_task: Task, task_update: TaskUpdate):
    # Update all attributes
    task_data = task_update.dict(exclude_unset=True)  # Only update provided fields
    for key, value in task_data.items():
        if key != "subTasks":  # Handle subtasks separately
            setattr(db_task, key, value)

    # Handle subtask updates
    if task_update.subTasks:
        for subtask_update in task_update.subTasks:
            # Check if subtask already exists
            statement = select(SubTask).where(
                (SubTask.id == subtask_update.id) & (SubTask.task_id == db_task.id)
            )
            db_subtask = db.exec(statement).all()
            print('checksubttask',db_subtask, len(db_subtask))
            if len(db_subtask) > 0:
                # Update existing subtask attributes
                subtask_data = subtask_update.dict(exclude_unset=True)
                for key, value in subtask_data.items():
                    setattr(db_subtask[0], key, value)
                db.add(db_subtask[0])
            else:
                # Add new subtask if it doesn't exist
                new_subtask = SubTask(  # Ensure the ID is set if provided
                    name=subtask_update.name,
                    completed=subtask_update.completed or False,
                    task_id=db_task.id  # Associate with the current task
                )
                db.add(new_subtask)


    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def remove_task(db: Session, task_id: str):
    db_task = db.get(Task, task_id)
    print(f"Removing task: {db_task}")
    if not db_task:
        return False
    else:
        db.delete(db_task)
        db.commit()
        return True
    return False

def remove_all_task(db: Session):
    # Use the session to execute a bulk delete
    statement = select(Task)
    tasks = db.exec(statement).all()

    if not tasks:
        print("No tasks found to remove.")
        return False

    # Remove each task
    for task in tasks:
        print(f"Removing task: {task.title}")
        db.delete(task)

    # Commit the changes to the database
    db.commit()
    print("All tasks removed successfully.")
    return True