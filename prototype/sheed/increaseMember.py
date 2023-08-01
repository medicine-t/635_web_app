import requests

url = "http://localhost"

def increaseMember():
    response = requests.post(f"{url}/v1/users/create/",params={"user_name" : "testUser"})
    user_id = response.json()["user_id"]

    requests.post(f"{url}/v1/rooms/{room_id}/join",params={"user_id": user_id})

def getRoomList():
        response = requests.get(f"{url}/v1/rooms/list")
        room_list = response.json()
        return room_list

room_id = getRoomList()[-1]["room_id"]

for _ in range(5):
    increaseMember()
    