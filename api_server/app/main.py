from fastapi import FastAPI,Response
from pydantic import BaseModel,UUID4
import datetime 
import uuid
app = FastAPI()

class User(BaseModel):
    user_id: UUID4
    user_name: str

class Room(BaseModel):
    room_id: UUID4
    room_name: str
    members: list[User]
    host_user : str
    start_time : datetime.time = None
    is_start : bool = False

class Idea(BaseModel):
    idea : str = ""
    num_eval : int = 0

class Sheet(BaseModel):
    id: UUID4
    room_id: UUID4
    user_id: UUID4
    ideas : list[Idea]

rooms:list[Room] = []
users:list[User] = []

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/v1/rooms/list")
async def get_room_list() -> list[Room]:
    return rooms

class CreateRoom(BaseModel):
    room_name: str
    user_id: UUID4

@app.post("/v1/rooms/create")
async def create_room(room_info: CreateRoom):
    rooms.append(
        Room(room_id=uuid.uuid4(),room_name=room_info.room_name,members=[],host_user=room_info.user_id)
        )
    return {"message": "success"}
    
@app.get("/v1/roooms/{room_id}")
async def get_room_info(room_id: UUID4) -> Room:
    ret: Room = None
    for room in rooms:
        if room.room_id == room_id:
            ret = room

    if ret == None:
        return Response(status_code=404)
    else :
        return ret

@app.post("/v1/users/create")
async def create_user(user_name: str) -> list[User]:
    users.append(User(user_name=user_name,user_id=uuid.uuid4()))
    return users

@app.get("/v1/users/{user_id}")
async def get_user_info(user_id: UUID4) -> User:
    ret: User = None
    for user in users:
        if user.user_id == user_id:
            ret = user

    if ret == None:
        return Response(status_code=404)
    else :
        return ret
    
@app.get("/v1/users/list")
async def get_user_list() -> list[User]:
    return users

@app.post("/v1/rooms/{room_id}/join")
async def join_room(room_id: UUID4,user_id: UUID4):
    room = await get_room_info(room_id)
    if len(room.members) >= 6:
        return Response(status_code=403)
    user = await get_user_info(user_id)
    room.members.append(user)
    return {"message": "success"}

@app.post("/v1/rooms/{room_id}/start")
async def start_room(room_id: UUID4) -> datetime.time:
    room = await get_room_info(room_id)
    if len(room.members) != 6:
        return Response(status_code=400)
    room.start_time = datetime.time() + datetime.time(second=5)
    return room.start_time
