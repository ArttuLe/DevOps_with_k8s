import logging
import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@project-db-svc:5432/todoapp")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
max_todo_len = 140
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    
class TodoCreate(BaseModel):
    title: str = Field(description="Title of the todo")

Base.metadata.create_all(bind=engine)
todos = list()

app = FastAPI()
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    body = await request.body()
    if body:
        logger.info(f"Body: {body.decode('utf-8')}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/todo")
def read_todos():
    session = SessionLocal()
    todos = session.query(Todo).all()
    session.close()
    logger.info(f"Returned {len(todos)} todos")
    return todos

@app.post("/todo")
def create_todo(todo: TodoCreate):
    logger.info(f"Creating a new todo: {todo.title}")
    session = SessionLocal()
    todo = Todo(title=todo.title)
    if len(todo.title) > max_todo_len:
        logger.warning(f"Todo creation failed. Title exceeds {max_todo_len}")
        raise HTTPException(status_code=400, detail=f"Title exceeds {max_todo_len} characters")
    session.add(todo)
    session.commit()
    logger.info(f"Todo created with id: {todo.id}")
    session.close()
    return {"message": "Todo created"}

@app.put("/todo/{todo_id}")
def update_todo(todo_id: int, completed: bool):
    session = SessionLocal()
    todo = session.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = completed
    session.commit()
    session.close()
    return {"message": "Todo updated"}

@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    session = SessionLocal()
    todo = session.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo doesnt exist")
    session.delete(todo)
    session.commit()
    session.close()
    return {"message": "Todo deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)), log_level="trace")