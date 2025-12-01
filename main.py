from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Models
class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)


# Crear tablas si no existen
Base.metadata.create_all(bind=engine)


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskDelete(BaseModel):
    id: int


class Task(TaskCreate):
    id: int

    class Config:
        orm_mode = True


# Authentication Token

valid_token = "secrettoken123"

security = HTTPBearer()


def get_Current_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme.lower() != "bearer" or credentials.credentials != valid_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing token",
        )



#  --- APP y dependencias ---
app = FastAPI(title="Taskify Demo API", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
def login(username: str, password: str):
    if username == "admin" and password == "password":
        return {"token": valid_token}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    
# Crud Operations

@app.get("/tasks", response_model=List[Task], dependencies=[Depends(get_Current_token)])
def list_tasks(db: Session = Depends(get_db), token: str = Depends(get_Current_token)):
    tasks = db.query(TaskDB).all()
    return tasks


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_Current_token)])
def create_task(task: TaskCreate, db: Session = Depends(get_db), token: str = Depends(get_Current_token)):
    db_task = TaskDB(title=task.title, description=task.description, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}", response_model=Task, dependencies=[Depends(get_Current_token)])
def get_task(task_id: int, db: Session = Depends(get_db), token: str = Depends(get_Current_token)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return task


@app.put("/tasks/{task_id}", response_model=Task, dependencies=[Depends(get_Current_token)])
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), token: str = Depends(get_Current_token)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description
    if task.completed is not None:
        db_task.completed = task.completed
    
    db.commit()
    db.refresh(db_task)
    return db_task

@app.patch("/tasks/{task_id}", response_model=Task)
def patch_task(task_id: int, partial: dict, db: Session = Depends(get_db), token: str = Depends(get_Current_token)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    # Aplicar sólo campos enviados
    if "titulo" in partial:
        task.titulo = partial["titulo"]
    if "descripcion" in partial:
        task.descripcion = partial["descripcion"]
    if "completado" in partial:
        task.completado = partial["completado"]
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), token: str = Depends(get_Current_token)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(task)
    db.commit()
    return None