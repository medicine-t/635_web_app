import requests
import datetime

class Idea():
    idea : str = ""
    num_eval : int = 0
        
class Model:
    def __init__(self) -> None:
        self.url = "http://localhost" # プログラマが設定
        self.room_id = "" #Controllerの_to_registrationでroom_idを設定する。
        self.user_id = "" #部屋参加登録時に更新
        self.room_name = ""
        self.phase_num = 0

    ### Room ###
    def getRoomList(self):
        response = requests.get(f"{self.url}/v1/rooms/list")
        room_list = response.json()
        return room_list
    
    def getRoom(self):
        response = requests.get(f"{self.url}/v1/rooms/{self.room_id}")
        print(response)
        room = response.json()
        return room
    
    def createRoom(self):
        response = requests.post(f"{self.url}/v1/rooms/create/{self.room_name}/{self.user_id}")
        if response.status_code != 200:
            return False
        self.room_id = response.json()["room_id"]
        return True
    

    def updateRoom(self) :
        response = requests.post(f"{self.url}/v1/room/update/",params={"user_id":self.user_id,"room_id":self.room_id})
        if response.status_code != 200:
            return False
        return True
    
    def startRoom(self) -> datetime.datetime:  
        response = requests.post(f"{self.url}/v1/rooms/{self.room_id}/start",params={"user_id":self.user_id})
        if response.status_code != 200:
            return False
        return True

    ### User ###
    def createUser(self, user_name: str):
        response = requests.post(f"{self.url}/v1/users/create/",params={"user_name" : user_name})
        if response.status_code != 200:
            return False 
        self.user_id = response.json()["user_id"]
        return True
    
    def registration(self):
        response = requests.post(f"{self.url}/v1/rooms/{self.room_id}/join",params={"user_id":self.user_id})
        if response.status_code != 200:
            return False
        return True
    
    ### Sheet ###

    def getSheetList(self):
        response = requests.get(f"{self.url}/v1/sheet/{self.room_id}")
        if response.status_code != 200:
            return False
        return response.json()
    
    def getSheet(self):
        sheets = self.getSheetList()
        sheet = None
        for s in sheets:
            if s["user_id"] == self.user_id:
                sheet = s
                break

        return sheet
    
    def setSheet(self, sheet):
        sheet["isUpdate"] = True
        response = requests.post(f"{self.url}/v1/sheet/update/",json=sheet)
        if response.status_code != 200:
            return False
        return True
    
    def edit_sheet(self, idea_texts):
        sheet = self.getSheet()
        ideas = []
        for text in idea_texts:
            idea = {"idea": text, "num_eval": 0}
            ideas.append(idea)

        sheet["ideas"][self.phase_num] = ideas
        return sheet