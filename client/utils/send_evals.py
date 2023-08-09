'''評価フェーズの最新のルームにおいて、シートを全て送信済み状態にするメソッド。'''
import requests
import random

url = "http://localhost"

# 最新のルーム取得
room_list = requests.get(f"{url}/v1/rooms/list").json()
room = room_list[-1]
room_id = room["room_id"]

# シートのリスト取得
sheet_list = requests.get(f"{url}/v1/sheet/{room_id}").json()

# 未送信のシートを全て送信する
for sheet in sheet_list:
    if not sheet["isUpdate"]:
        rand_num = random.randrange(6)
        for i in range(3):
            sheet["ideas"][rand_num][i]["num_eval"] += 1
        sheet["isUpdate"] = True
        requests.post(f"{url}/v1/sheet/update/",json=sheet)