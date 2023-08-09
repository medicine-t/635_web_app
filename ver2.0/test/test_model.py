import requests
import datetime
import unittest
import time
import sys
sys.path.append("../")
from app.models import Model


URL = "http://localhost"
ROOM_NAME = "testRoom"
USER_NAME = "test"

class ModelTest(unittest.TestCase):
    '''モデルのメソッドの単体テストを行うクラス。'''
    def setUp(self):
        # このメソッドは，テストごとに事前に実行される
        # ホストユーザーの作成
        self.user = requests.post(f"{URL}/v1/users/create/",params={"user_name" : USER_NAME}).json()
        # テスト用ルームの作成
        room_id = requests.post(f"{URL}/v1/rooms/create/{ROOM_NAME}/{self.user['user_id']}").json()["room_id"]
        # ユーザーをテスト用ルームに参加させる。
        requests.post(f"{URL}/v1/rooms/{room_id}/join", params={"user_id": self.user["user_id"]})
        # テスト用ルームをフィールドに保存
        self.room = requests.get(f"{URL}/v1/rooms/{room_id}").json()
        # モデルの作成
        self.model = Model()

        self.model.user_id = self.user["user_id"]
        self.model.room_id = self.room["room_id"]

    def testGetRoomList(self):
        response = requests.get(f"{URL}/v1/rooms/list")
        expect = response.json()
        result = self.model.getRoomList() 
        self.assertEqual(result, expect)

    def testGetRoom(self):
        expect = self.room
        result = self.model.getRoom()
        self.assertEqual(result, expect)

    def testCreateRoom(self):
        self.model.room_name = ROOM_NAME
        self.model.user_id = self.user["user_id"]
        self.model.createRoom()

        # 現在作成されているルームで一番新しく作成されたルームの取得
        response = requests.get(f"{URL}/v1/rooms/list")
        expect = response.json()[-1]["room_id"]
        result = self.model.room_id
        self.assertEqual(result, expect)

    def testUpdateRoom(self):
        room_id = self.room["room_id"]

        participants = []
        # ルームを満室にする。
        for _ in range(5):
            participants.append(
                requests.post(f"{URL}/v1/users/create/",params={"user_name" : USER_NAME}).json()
            )
            requests.post(f"{URL}/v1/rooms/{room_id}/join", params={"user_id": participants[-1]["user_id"]})

        # ルーム開始要求を出してから、カウントダウン
        response = requests.post(f"{URL}/v1/rooms/{room_id}/start",params={"user_id": self.user["user_id"]}).json()
        start_time = datetime.datetime.strptime(response["start_time"], '%Y-%m-%dT%H:%M:%S.%f') + datetime.timedelta(hours=9)
        # 本来は、waiting_time分待機する。
        waiting_time = start_time - datetime.datetime.now()
        
        # 全員が1枚目のシートをもらう
        sheets = requests.get(f"{URL}/v1/sheet/{room_id}").json()

        expect = False
        result = self.model.updateRoom()
        # まだ全員がシートを提出していないので、ルームアップデート要求は拒否される。
        self.assertEqual(result, expect)

        # シートの情報更新 & 送信
        for sheet in sheets:
            # シートの最初の行に3つアイデアを記入
            sheet["ideas"][0] = [{"idea": "test", "num_eval": 0}, {"idea": "test", "num_eval": 0}, {"idea": "test", "num_eval": 0}]
            sheet["isUpdate"] = True
            requests.post(f"{URL}/v1/sheet/update/",json=sheet)

        expect = True
        result = self.model.updateRoom()
        # 全員がシートを提出したので、ルームアップデート要求が受け入れられる。
        self.assertEqual(result, expect)

        room = requests.get(f"{URL}/v1/rooms/{room_id}").json()
        expect = 1
        result = room["phase_num"]
        # ルームのフェーズ状態が、0->1にインクリメントされる。
        self.assertEqual(result, expect)

        sheets = requests.get(f"{URL}/v1/sheet/{room_id}").json()
        for sheet in sheets:
            expect = False
            result = sheet["isUpdate"]
            # シートの提出済みフラグがFalseに設定される。
            self.assertEqual(result, expect)

    def testStartRoom(self):
        room_id = self.room["room_id"]

        # ルームを満室にする。
        for _ in range(5):
            user = requests.post(f"{URL}/v1/users/create/",params={"user_name" : USER_NAME}).json()
            requests.post(f"{URL}/v1/rooms/{room_id}/join", params={"user_id": user["user_id"]})

        self.model.startRoom()
        room = requests.get(f"{URL}/v1/rooms/{room_id}").json()
        expect = True
        result = room["is_start"]
        self.assertEqual(result, expect)

    def testCreateUser(self):
        self.model.createUser(USER_NAME)
        new_user = requests.get(f"{URL}/v1/users/list").json()[-1]
        expect = new_user["user_id"]
        result = self.model.user_id
        self.assertEqual(result, expect)

    def testJoinRoom(self):
        # 部屋の作成
        host_user = requests.post(f"{URL}/v1/users/create/",params={"user_name" : USER_NAME}).json()
        room_id = requests.post(f"{URL}/v1/rooms/create/{ROOM_NAME}/{host_user['user_id']}").json()["room_id"]
        requests.post(f"{URL}/v1/rooms/{room_id}/join", params={"user_id": host_user["user_id"]})

        # 作成した部屋に参加する。
        self.model.room_id = room_id
        self.model.joinRoom()
        room = requests.get(f"{URL}/v1/rooms/{room_id}").json()
        new_member = room["members"][-1]
        expect = new_member["user_id"]
        result = self.model.user_id
        self.assertEqual(result, expect)

    def testGetSheetList(self):
        result = self.model.getSheetList()
        expect = requests.get(f"{URL}/v1/sheet/{self.room['room_id']}").json()
        self.assertEqual(result, expect)

    def getSheet(self):
        room_id = self.room["room_id"]

        # ルームを満室にする。
        for _ in range(5):
            user = requests.post(f"{URL}/v1/users/create/",params={"user_name" : USER_NAME}).json()
            requests.post(f"{URL}/v1/rooms/{room_id}/join", params={"user_id": user["user_id"]})

        # ルーム開始要求を出してから、カウントダウン
        response = requests.post(f"{URL}/v1/rooms/{room_id}/start",params={"user_id": self.user["user_id"]}).json()
        start_time = datetime.datetime.strptime(response["start_time"], '%Y-%m-%dT%H:%M:%S.%f') + datetime.timedelta(hours=9)
        # 本来は、waiting_time分待機する。
        waiting_time = start_time - datetime.datetime.now()
        

        sheet = self.model.getSheet()
        expect = self.model.user_id
        result = sheet["user_id"]

        self.assertEqual(result, expect)

    def testSetSheet(self):
        room_id = self.room["room_id"]

        # ルームを満室にする。
        for _ in range(5):
            user = requests.post(f"{URL}/v1/users/create/",params={"user_name" : USER_NAME}).json()
            requests.post(f"{URL}/v1/rooms/{room_id}/join", params={"user_id": user["user_id"]})

        # ルーム開始要求を出してから、カウントダウン
        response = requests.post(f"{URL}/v1/rooms/{room_id}/start",params={"user_id": self.user["user_id"]}).json()
        start_time = datetime.datetime.strptime(response["start_time"], '%Y-%m-%dT%H:%M:%S.%f') + datetime.timedelta(hours=9)
        # 本来は、waiting_time分待機する。
        waiting_time = start_time - datetime.datetime.now()

        # シートを取得
        sheets = requests.get(f"{URL}/v1/sheet/{room_id}").json()
        sheet = None
        for s in sheets:
            if s["user_id"] == self.model.user_id:
                sheet = s
                break
        
        # シートを編集
        sheet["ideas"][0] = [{"idea": "test", "num_eval": 0}, {"idea": "test", "num_eval": 0}, {"idea": "test", "num_eval": 0}]
        
        # シート送信
        self.model.setSheet(sheet)

        # APIサーバーから更新したシート取得
        sheets = requests.get(f"{URL}/v1/sheet/{room_id}").json()
        sended_sheet = None
        for s in sheets:
            if s["user_id"] == self.model.user_id:
                sended_sheet = s
                break
        
        expect = True
        result = sended_sheet["isUpdate"]

        self.assertEqual(result, expect)

        sheet["isUpdate"] = True
        self.assertEqual(sended_sheet, sheet)

    def testEditSheet(self):
        room_id = self.room["room_id"]

        # ルームを満室にする。
        for _ in range(5):
            user = requests.post(f"{URL}/v1/users/create/",params={"user_name" : USER_NAME}).json()
            requests.post(f"{URL}/v1/rooms/{room_id}/join", params={"user_id": user["user_id"]})

        # ルーム開始要求を出してから、カウントダウン
        response = requests.post(f"{URL}/v1/rooms/{room_id}/start",params={"user_id": self.user["user_id"]}).json()
        start_time = datetime.datetime.strptime(response["start_time"], '%Y-%m-%dT%H:%M:%S.%f') + datetime.timedelta(hours=9)
        # 本来は、waiting_time分待機する。
        waiting_time = start_time - datetime.datetime.now()

        # シートを取得
        sheets = requests.get(f"{URL}/v1/sheet/{room_id}").json()
        sheet = None
        for s in sheets:
            if s["user_id"] == self.model.user_id:
                sheet = s
                break
        
        # 手作業でシートを編集
        sheet["ideas"][0] = [{"idea": "test", "num_eval": 0}, {"idea": "test", "num_eval": 0}, {"idea": "test", "num_eval": 0}]
        expect = sheet

        # モデルでシートを編集
        idea_texts = ["test", "test", "test"]
        result = self.model.editSheet(idea_texts)
        self.assertEqual(result, expect)

if __name__ == "__main__":
    unittest.main()