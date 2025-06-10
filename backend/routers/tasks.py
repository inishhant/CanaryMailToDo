from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
import crud, schemas
from datetime import date, time

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks", response_model=schemas.Task)
def create(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@router.get("/tasks", response_model=List[schemas.Task])
def read_all(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@router.get("/tasks/{task_id}", response_model=schemas.Task)
def read_one(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update(task_id: int, task_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}")
def delete(task_id: int, db: Session = Depends(get_db)):
    task = crud.delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

@router.get("/search", response_model=List[schemas.Task])
def search(
    tag: Optional[str] = None,
    text: Optional[str] = None,
    date: Optional[date] = None,
    day: Optional[str] = None,
    time: Optional[time] = None,
    db: Session = Depends(get_db)
):
    return crud.search_tasks(db, tag, text, date, day, time)
