from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from sqlalchemy.orm import Session
from sqlalchemy import select
import models
import database
from pydantic import BaseModel, ConfigDict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,  # type: ignore
    # allow_origins=["*"],  # Разрешить все источники (но это работает только для HTTP запросов)
    allow_origins=[
        "https://sibplc-kis3.ru",
        "http://localhost:3000",
        "http://localhost:80",
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)


class TaskCreate(BaseModel):
    name: str


class TaskResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(database.get_db)):
    db_task = models.Task(name=task.name)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks/", response_model=list[TaskResponse])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    stmt = select(models.Task).offset(skip).limit(limit)
    result = db.execute(stmt)
    return list(result.scalars().all())


# noinspection PyTypeChecker
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    stmt = select(models.Task).where(models.Task.id == task_id)
    result = db.execute(stmt)
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"ok": True}


# для автоматического перезапуска приложения при изменении кода
if __name__ == "__main__":
    # uvicorn.run("main:app", reload=True)
    # asyncio.run(test_connection())

    # прямой доступ всем желающим минуя NGINX прям по HTTP
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    # Доступ только из localhost. NGINX будет передавать запросы на 127.0.0.1:8000
    # более безопасный подход для production
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
