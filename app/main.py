import os
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from .database import Task as TaskModel, get_db, init_db
from .models import TaskCreate, TaskUpdate, TaskResponse
from .cache import cache
from typing import List

app = FastAPI(title="Task Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    await cache.init_redis(redis_url)

@app.on_event("shutdown")
async def shutdown():
    await cache.close()

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    db_task = TaskModel(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

@app.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskModel))
    tasks = result.scalars().all()
    return list(tasks)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    # Try to get from cache first
    cached_task = await cache.get_task(task_id)
    if cached_task:
        return TaskResponse(**cached_task)

    # If not in cache, get from database
    result = await db.execute(select(TaskModel).filter(TaskModel.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Cache the task
    await cache.set_task(task_id, TaskResponse.model_validate(task))
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db)):
    update_data = {k: v for k, v in task_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid update data provided")
    
    result = await db.execute(
        update(TaskModel)
        .where(TaskModel.id == task_id)
        .values(**update_data)
        .returning(TaskModel)
    )
    updated_task = result.scalar_one_or_none()
    
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.commit()
    
    # Invalidate cache
    await cache.invalidate_task(task_id)
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        delete(TaskModel).where(TaskModel.id == task_id)
    )
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.commit()
    
    # Invalidate cache
    await cache.invalidate_task(task_id)
    return None
