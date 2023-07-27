import tkinter as tk

class TestFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.label = None
        self.button = None
        self.wait_button = None

    def setup(self):
        self.label = tk.Label(self, text="oiuy")
        self.label.pack()

        self.button = tk.Button(self, text="test button")
        self.button.pack()

class StartFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomList = []
        self.ToNameRoom = None
        self.CreatRoom = None

    def setup(self,roomlist: list):
        for room in roomlist:
            name = room["room_name"]
            room_id = room["room_id"]
            self.RoomList.append(tk.Button(self, f"{name}({room_id})"))
            self.RoomList.pack()

        self.ToNameRoom = tk.Entry(self, fg='gray', bg="white")
        self.ToNameRoom.pack()

        self.CreatRoom = tk.Button(self, text="名前作成")
        self.CreatRoom.pack()

class RegistrationFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.UserName = None
        self.Registration = None
        self.RoomName = None

    def setup(self,room: dict):
        room_name = room["room_name"]
        self.RoomName =tk.Label(self,room_name)
        self.RoomName.pack()

        self.UserName = tk.Entry(self, fg='gray', bg="white")
        self.UserName.pack()

        self.Registration = tk.Button(self, text="登録")
        self.Registration.pack()

class StandbyFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomName = None
        self.NumberOfMenbers = None
        self.SessionStart = None

    def setup(self,room: dict):
        room_name = room["name"]
        self.RoomName =tk.Label(self,room_name)
        self.RoomName.pack()

        numberofmembers = len(room["members"])
        self.NumberOfMenbers = tk.Label(self, numberofmembers+"人")
        self.NumberOfMenbers.pack()

        self.Registration = tk.Button(self, text="開始")
        self.Registration.pack()