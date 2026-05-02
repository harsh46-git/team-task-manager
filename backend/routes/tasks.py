from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Task, Project, User, RoleEnum, StatusEnum
from schemas import TaskCreate, TaskUpdate, TaskOut
from auth import get_current_user, require_admin

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("/", response_model=TaskOut)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if payload.assignee_id:
        assignee = db.query(User).filter(User.id == payload.assignee_id).first()
        if not assignee:
            raise HTTPException(status_code=404, detail="Assignee not found")
    task = Task(**payload.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=List[TaskOut])
def list_tasks(
    project_id: Optional[int] = None,
    assignee_id: Optional[int] = None,
    status: Optional[StatusEnum] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Task)
    # Members only see their own tasks; admins see all
    if current_user.role != RoleEnum.admin:
        query = query.filter(Task.assignee_id == current_user.id)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if assignee_id:
        query = query.filter(Task.assignee_id == assignee_id)
    if status:
        query = query.filter(Task.status == status)
    return query.all()


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Task)
    if current_user.role != RoleEnum.admin:
        query = query.filter(Task.assignee_id == current_user.id)
    all_tasks = query.all()
    now = datetime.utcnow()
    return {
        "total": len(all_tasks),
        "todo": sum(1 for t in all_tasks if t.status == StatusEnum.todo),
        "in_progress": sum(1 for t in all_tasks if t.status == StatusEnum.in_progress),
        "done": sum(1 for t in all_tasks if t.status == StatusEnum.done),
        "overdue": sum(
            1 for t in all_tasks
            if t.due_date and t.due_date < now and t.status != StatusEnum.done
        ),
    }


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Members can only update their own task's status
    if current_user.role != RoleEnum.admin:
        if task.assignee_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only update your own tasks")
        # Members can only change status
        if payload.status is not None:
            task.status = payload.status
    else:
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
