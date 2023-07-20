from fastapi import FastAPI,Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel,UUID4
from typing import Optional
import datetime 
import uuid
import asyncio
app = FastAPI()

class User(BaseModel):
    user_id: UUID4
    user_name: str

class Room(BaseModel):
    room_id: UUID4
    room_name: str
    members: list[User]
    host_user : UUID4
    start_time : datetime.time = None
    is_start : bool = False

class Idea(BaseModel):
    idea : str = ""
    num_eval : int = 0

class Sheet(BaseModel):
    id: UUID4
    room_id: UUID4
    user_id: UUID4 # writing user id
    ideas : list[Idea] = [[Idea()] * 3 for i in range(6)]

rooms:list[Room] = []
users:list[User] = []
sheets: list[Sheet] = []

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/v1/rooms/list")
async def get_room_list() -> list[Room]:
    return rooms

@app.post("/v1/room/update/{room_id}")
async def update_room(room_id:UUID4):
    room:Room = await get_room_info(room_id)
    for s in sheets:
        if s.room_id == room_id:
            s.user_id = (room.members.index(s.user_id) + 1) % len(room.members)
            break

@app.post("/v1/rooms/create/{room_name}/{user_id}")
async def create_room(room_name:str, user_id:UUID4):
    rooms.append(
        Room(room_id=uuid.uuid4(),room_name=room_name,members=[],host_user=user_id)
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

@app.get("/v1/users/list")
async def get_user_list():
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
    if type(room) == Response:
        return JSONResponse(status_code=404,content={"message":"room not found"})
    if len(room.members) != 6:
        return JSONResponse(status_code=403,content={"message":"not enough members now"})
    for user in room.members:
        await create_sheet(room_id,user.user_id)
    room.start_time = datetime.datetime.time() + datetime.timedelta(seconds=5)
    return room.start_time

#@app.post("/v1/sheet/create/{room_id}/{user_id}")
async def create_sheet(room_id: UUID4,user_id: UUID4):
    sheet = Sheet(id=uuid.uuid4(),room_id=room_id,user_id=user_id)
    sheets.append(sheet)
    return

@app.post("/v1/sheet/update/")
async def set_sheet(sheet:Sheet):
    for s in sheets:
        if s.id == sheet.id:
            s = sheet
            break
    return

