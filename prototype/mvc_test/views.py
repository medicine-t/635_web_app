import tkinter as tk
from tkinter import ttk

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
        self.CreateRoom = None

    def setup(self, roomlist: list):
        for room in roomlist:
            name = room["room_name"]
            room_id = room["room_id"]
            self.RoomList.append(tk.Button(self, text=f"{name}.{room_id}", width=20, anchor="w"))
            self.RoomList[-1].pack()

        self.ToNameRoom = tk.Entry(self, bg="white")
        self.ToNameRoom.pack()

        self.CreateRoom = tk.Button(self, text="名前作成")
        self.CreateRoom.pack()

class RegistrationFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.UserName = None
        self.Registration = None
        self.RoomName = None

    def setup(self, room_name: str):
        self.RoomName =tk.Label(self, text=room_name)
        self.RoomName.pack()

        self.UserName = tk.Entry(self, bg="white")
        self.UserName.pack()

        self.Registration = tk.Button(self, text="登録")
        self.Registration.pack()

class StandbyFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomName = None
        self.NumberOfMenbers = None
        self.SessionStart = None

    def setup(self, room: dict):
        room_name = room["name"]
        self.RoomName =tk.Label(self, text=room_name)
        self.RoomName.pack()

        number_of_members = len(room["members"])
        self.NumberOfMenbers = tk.Label(self, text=number_of_members+"人")
        self.NumberOfMenbers.pack()

        self.Registration = tk.Button(self, text="開始")
        self.Registration.pack()

class CountdownFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomName = None
        self.startRemainTime = None

    def setup(self, room: dict):
        room_name = room["name"]
        self.RoomName =tk.Label(self, text=room_name)
        self.RoomName.pack()

        self.startRemainTime =tk.Label(self)
        self.startRemainTime.pack()

class WritingFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomName = None
        self.ideaTextBox = list
        self.table = tk.Frame(self)
        self.table.pack()

    def setup(self, room: dict, ideas: list, row_wiritng: int): #row_writing 書き込みを行う行の行番号
        room_name = room["name"]
        self.RoomName =tk.Label(self, text=room_name)
        self.RoomName.pack()

        for i, row in enumerate(ideas):
            for j, idea in enumerate(row):
                if j == row_wiritng:
                    textbox = tk.Entry(self.table, bg="white")
                    textbox.grid(row=i, column=j)
                    self.ideaTextBox.append(textbox)
                else:
                    label = tk.Label(self.table, text=idea["idea"])
                    label.grid(row=i, column=j)

class ReviewFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomName = None
        self.evaluate = [[] for _ in range(6)]

        self.table = None

    def setup(self, room: dict, ideas: list):
        self.table = tk.Frame(self)
        self.table.pack()
        
        room_name = room["name"]
        self.RoomName =tk.Label(self, text=room_name)
        self.RoomName.pack()

        for i, row in enumerate(ideas):
            for j, idea in enumerate(row):
                checkbutton = tk.Checkbutton(self.table, text=idea["idea"])
                checkbutton.grid(row=i, column=j)
                self.evaluate.append(checkbutton)

class RankingFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomName = None
        self.exitButton = None
        self.rankingBoard = None

    def setup(self, room: dict, ranking: list):
        room_name = room["name"]
        self.RoomName =tk.Label(self, text=room_name)
        self.RoomName.pack()
        column = ("place", "idea", "score", "author")
        self.rankingBoard = ttk.Treeview(self, columns=column)
        self.rankingBoard.column('place',anchor='center', width=50)
        self.rankingBoard.column('idea', anchor='w', width=120)
        self.rankingBoard.column('score',anchor='center', width=80)
        self.rankingBoard.column('author', anchor='center', width=80)

        self.rankingBoard.heading('place',text='Place', anchor='center')
        self.rankingBoard.heading('idea', text='Idea',anchor='center')
        self.rankingBoard.heading('score', text='Score', anchor='center')
        self.rankingBoard.heading('author',text='Author', anchor='center')
        
        for i, idea in ranking:
            continue