from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Пустой список пользователей
users = []

# Класс модели пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# GET запрос для получения всех пользователей
@app.get("/users", response_model=List[User])
async def get_users():
    return users

# POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}", response_model=User)
async def create_user(username: str, age: int):
    # Определяем id нового пользователя
    user_id = 1 if not users else users[-1].id + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

# PUT запрос для обновления существующего пользователя
@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            removed_user = users.pop(index)
            return removed_user
    raise HTTPException(status_code=404, detail="User was not found")