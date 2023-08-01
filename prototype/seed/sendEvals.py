import requests
from pydantic import BaseModel,UUID4
from typing import List

url = "http://localhost"
idea_texts = ["test", "test", "test"]
user_id = ""

def getRoomList():      
    response = requests.get(f"{url}/v1/rooms/list")
    room_list = response.json()
    return room_list

def getSheetList(room_id):
    response = requests.get(f"{url}/v1/sheet/{room_id}")
    if response.status_code != 200:
        return False
    return response.json()

def sendEvals(room):
    sheetList = getSheetList(room["room_id"])
    for i, sheet in enumerate(sheetList):
        if sheet["user_id"] == room["host_user"]:
            print(i)
            continue

        sheet["ideas"][i][0]["num_eval"] += 1
        sheet["isUpdate"] = True
        response = requests.post(f"{url}/v1/sheet/update/",json=sheet)

room = getRoomList()[-1]

sendEvals(room)
