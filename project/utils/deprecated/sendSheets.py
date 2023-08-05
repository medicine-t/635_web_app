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

def sendSheets(room):
    sheetList = getSheetList(room["room_id"])
    phase_num = room["phase_num"]
    for i, sheet in enumerate(sheetList):
        if sheet["user_id"] == room["host_user"]:
            print(i)
            continue

        ideas = []
        for text in idea_texts:
            idea = {"idea": text, "num_eval": 0}
            ideas.append(idea)
        
        sheet["ideas"][phase_num] = ideas
        sheet["isUpdate"] = True
        response = requests.post(f"{url}/v1/sheet/update/",json=sheet)

room = getRoomList()[-1]

sendSheets(room)
