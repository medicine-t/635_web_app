'''最新のルームのメンバーを満員にするプログラム'''
import requests

url = "http://localhost"

# 最新のルーム取得
room_list = requests.get(f"{url}/v1/rooms/list").json()
room = room_list[-1]

# ルームid, メンバー数取得
room_id = room["room_id"]
num_members = len(room["members"])

# メンバーがフルになるまで、部屋にメンバーを追加する。
for _ in range(max(0, 6 - num_members)):
    user_id = requests.post(f"{url}/v1/users/create/",params={"user_name" : "testUser"}).json()["user_id"]
    requests.post(f"{url}/v1/rooms/{room_id}/join",params={"user_id": user_id})
    