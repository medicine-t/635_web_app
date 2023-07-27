import requests

class TestModel:
    def test(self, text):
        print(text)

    def waitng_print(self):
        print("I'm wainting!")
        
class Model:
    def __init__(self) -> None:
        self.url = "" # プログラマが設定
        self.room_id = "" #Controllerの_to_registrationでroom_idを設定する。
        self.user_id = "" #部屋参加登録時に更新

    def getRoomList(self):
        response = requests.get(self.url + "/v1/rooms/list")
        room_list = response.json()
        return room_list
    
    def getRoom(self):
        pass
    
    def createRoom(self):
        pass