'''記入フェーズの最新のルームにおいて、シートを全て送信済み状態にするメソッド。'''
import requests

url = "http://localhost"

# 最新のルーム取得
room_list = requests.get(f"{url}/v1/rooms/list").json()
room = room_list[-1]
room_id = room["room_id"]
phase_num = room["phase_num"]

# シートのリスト取得
sheet_list = requests.get(f"{url}/v1/sheet/{room_id}").json()

# 未送信のシートを全て送信する
for sheet in sheet_list:
    if not sheet["isUpdate"]:
        sheet["ideas"][phase_num] = [{"idea": "testIdea", "num_eval": 0}, {"idea": "testIdea", "num_eval": 0}, {"idea": "testIdea", "num_eval": 0}]
        sheet["isUpdate"] = True
        requests.post(f"{url}/v1/sheet/update/",json=sheet)
        
