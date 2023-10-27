from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
from models import User, Gender, Role, UpdateUser
from typing import List

app  = FastAPI()

db: List[User] =[
    User(
        id="7eb3a8b2-ca4e-465e-be8b-e9f0bf04baf4", 
        first_name="Jamila",
        middle_name="bin",
        last_name="Ahmed",
        gender=Gender.female,
        roles=[Role.student]
    ),
    User(
        id="2ad2a3c4-a677-46c4-a33e-84185ba43f10", 
        first_name="Alex",
        middle_name="bin",
        last_name="Jones",
        gender=Gender.female,
        roles=[Role.admin, Role.user]
    )
]

@app.get('/')
def root():
    return {"Hello": "World"}

@app.get('/api/v1/users')
async def fetch_users():
    return db; 

@app.post('/api/v1/users')
async def register_user(user:User):
    db.append(user)
    return {"id": user.id}

@app.delete('/api/v1/users/{user_id}')
async def delete_user(user_id:UUID):
    for user in db:
        print(user)
        if user.id == user_id:
            db.remove(user)
            return {"Message": "deleted"}
    raise HTTPException(status_code=404, detail=f"user with id:{user_id} does not exists.")


@app.put('/api/v1/users/{user_id}')
async def update_user(user_update: UpdateUser, user_id:UUID):
    for user in db:
        if user_id == user.id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404, detail=f"user with id: {user_id} does not exists."
    )