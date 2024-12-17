from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
from typing import List, Annotated

app = FastAPI()

# Пустой список пользователей
users = []

# Класс модели пользователя
class User(BaseModel):
    id: int
    username: str
    age: conint(ge=0)  # Возраст должен быть неотрицательным

# GET запрос для получения всех пользователей
@app.get("/users", response_model=List[User])
async def get_users():
    return users

# POST запрос для добавления нового пользователя
@app.post("/user/", response_model=User)
async def create_user(user: Annotated[User, ...]):  # Используем Annotated для валидации
    # Определяем id нового пользователя
    user_id = 1 if not users else users[-1].id + 1
    new_user = User(id=user_id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user

# PUT запрос для обновления существующего пользователя
@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, user: Annotated[User, ...]):  # Используем Annotated для валидации
    for existing_user in users:
        if existing_user.id == user_id:
            existing_user.username = user.username
            existing_user.age = user.age
            return existing_user
    raise HTTPException(status_code=404, detail="User was not found")

# DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for index, existing_user in enumerate(users):
        if existing_user.id == user_id:
            removed_user = users.pop(index)
            return removed_user
    raise HTTPException(status_code=404, detail="User was not found")