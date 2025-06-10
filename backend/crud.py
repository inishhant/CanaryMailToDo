from sqlalchemy.orm import Session
from models import Task, Tag
from schemas import TaskCreate
from datetime import datetime

def get_or_create_tag(db: Session, name: str):
    tag = db.query(Tag).filter_by(name=name).first()
    if not tag:
        tag = Tag(name=name)
        db.add(tag)
    return tag

def create_task(db: Session, task: TaskCreate):
    tag_objs = [get_or_create_tag(db, t) for t in task.tags]
    db_task = Task(
        title=task.title,
        description=task.description,
        date=task.date,
        is_completed=task.is_completed,
        tags=tag_objs
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session):
    return db.query(Task).all()

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db: Session, task_id: int, data: TaskCreate):
    task = get_task(db, task_id)
    if not task:
        return None
    for attr, value in data.dict(exclude_unset=True).items():
        if attr == 'tags':
            task.tags = [get_or_create_tag(db, t) for t in value]
        else:
            setattr(task, attr, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    if not task:
        return None
    db.delete(task)
    db.commit()
    return task

def search_tasks(db: Session, tag=None, text=None, date=None, day=None, time=None):
    query = db.query(Task)
    if tag:
        tag_obj = db.query(Tag).filter_by(name=tag).first()
        if tag_obj:
            query = query.filter(Task.tags.contains(tag_obj))
        else:
            return []
    if text:
        like_text = f"%{text}%"
        query = query.filter((Task.title.ilike(like_text)) | (Task.description.ilike(like_text)))
    if date:
        query = query.filter(Task.date == date)
    return query.all()
