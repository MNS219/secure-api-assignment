from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)
from jose import jwt, JWTError
from pydantic import BaseModel

app = FastAPI()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

fake_user = {
    "username": "admin",
    "password": "admin123"
}

tasks = []

class Task(BaseModel):
    title: str


@app.get("/")
def home():
    return {"message": "API Running"}


@app.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):

    if (
        data.username != fake_user["username"]
        or data.password != fake_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = jwt.encode(
        {"sub": data.username},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def verify_token(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


@app.get("/tasks")
def get_tasks(user=Depends(verify_token)):
    return tasks


@app.post("/tasks")
def create_task(
    task: Task,
    user=Depends(verify_token)
):
    tasks.append(task.dict())

    return {
        "message": "Task created",
        "task": task
    }