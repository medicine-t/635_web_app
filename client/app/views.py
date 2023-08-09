import tkinter as tk
from tkinter import ttk

class StartFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomList = []
        self.ToNameRoom = None
        self.CreateRoom = None
        self.titleFrame = None
        self.roomListFrame = None
        self.roomListLabel = None

    def setup(self, roomlist: list):
        self.titleFrame = tk.Frame(self)
        self.titleFrame.pack(side="left")

        self.roomListFrame = tk.Frame(self)
        self.roomListFrame.pack(side="left")

        self.roomListLabel = tk.Label(self.roomListFrame, text="ルーム一覧", relief=tk.SOLID, font=("normal", 20))
        self.roomListLabel.pack()

        for room in roomlist:
            if len(room["members"]) >= 6:
                continue
            name = room["room_name"]
            room_id = room["room_id"]
            self.RoomList.append(tk.Button(self.roomListFrame, text=f"{name}({room_id})", width=20, anchor="w", font=("normal", 20)))
            self.RoomList[-1].pack()
        
        self.ToNameRoom = tk.Entry(self.titleFrame, bg="white", relief=tk.RIDGE, width=30, font=("normal", 20))
        self.ToNameRoom.pack()

        self.CreateRoom = tk.Button(self.titleFrame, text="ルーム作成", bg="white", relief=tk.RIDGE, width=10, font=("normal", 20))
        self.CreateRoom.pack()
    
    def update(self, roomlist: list):
        for room_button in self.RoomList:
            room_button.destroy()
        
        for room in roomlist:
            if len(room["members"]) >= 6:
                continue
            name = room["room_name"]
            room_id = room["room_id"]
            self.RoomList.append(tk.Button(self.roomListFrame, text=f"{name}({room_id})", width=20, anchor="w", font=("normal", 20)))
            self.RoomList[-1].pack()

class RegistrationFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.UserName = None
        self.Registration = None
        self.RoomName = None

    def setup(self, room_name: str):
        self.RoomName =tk.Label(self, text=room_name, relief=tk.GROOVE)
        self.RoomName.pack()

        self.UserName = tk.Entry(self, bg="white", relief=tk.RIDGE)
        self.UserName.pack()

        self.Registration = tk.Button(self, text="登録", relief=tk.RIDGE)
        self.Registration.pack()

class StandbyFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomName = None
        self.NumberOfMenbers = None
        self.SessionStart = None

    def setup(self, room: dict):
        room_name = room["room_name"]
        self.RoomName =tk.Label(self, text=room_name, relief=tk.GROOVE)
        self.RoomName.pack()

        number_of_members = len(room["members"])
        self.NumberOfMenbers = tk.Label(self, text=f"{number_of_members}人", relief=tk.RIDGE)
        self.NumberOfMenbers.pack()

        self.Registration = tk.Button(self, text="開始", relief=tk.RIDGE)
        self.Registration.pack()

    def update(self, room: dict):
        number_of_members = len(room["members"])
        self.NumberOfMenbers["text"] = f"{number_of_members}人"

class CountdownFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomName = None
        self.startRemainTime = None

    def setup(self, room: dict, start_time: int):
        room_name = room["room_name"]
        self.RoomName =tk.Label(self, text=room_name, relief=tk.GROOVE)
        self.RoomName.pack()

        self.startRemainTime = tk.Label(self, text=f"{start_time}秒後に開始します。", relief=tk.RIDGE)
        self.startRemainTime.pack()

class WritingFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomName = None
        self.ideaTextBox = []
        self.labels = []
        self.table = tk.Frame(self, width=500)

    def setup(self, room: dict, ideas: list, row_wiritng: int): #row_writing 書き込みを行う行の行番号
        room_name = room["room_name"]
        self.RoomName =tk.Label(self, text=room_name, relief=tk.GROOVE)
        self.RoomName.pack()

        for i, row in enumerate(ideas):
            for j, idea in enumerate(row):
                if i == row_wiritng:
                    textbox = tk.Entry(self.table, bg="white", relief=tk.RIDGE, width=20)
                    textbox.grid(row=i, column=j)
                    self.ideaTextBox.append(textbox)
                else:
                    label = tk.Label(self.table, text=idea["idea"], relief=tk.RIDGE, width=20)
                    label.grid(row=i, column=j)
                    self.labels.append(label)

        self.table.pack()

    def update(self, room: dict, ideas: list, row_wiritng: int):
        self.RoomName.destroy()
        for textbox in self.ideaTextBox:
            textbox.destroy()
        self.table.destroy()

        for label in self.labels:
            label.destroy()

        self.RoomName = None
        self.ideaTextBox = []
        self.labels = []
        self.table = tk.Frame(self, width=500)

        self.setup(room, ideas, row_wiritng)

class ReviewFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomName = None
        self.evaluate = [[tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()] for _ in range(6)]
        self.checkbuttons = [[] for _ in range(6)]
        self.table = None

    def setup(self, room: dict, ideas: list):
        self.table = tk.Frame(self)
        
        room_name = room["room_name"]
        self.RoomName =tk.Label(self, text=room_name, relief=tk.GROOVE)
        self.RoomName.pack()

        for i, row in enumerate(ideas):
            for j, idea in enumerate(row):
                checkbutton = tk.Checkbutton(self.table, text=idea["idea"], relief=tk.RIDGE, width=20, variable=self.evaluate[i][j])
                checkbutton.grid(row=i, column=j)
                self.checkbuttons[i].append(checkbutton)

        self.table.pack()

    def update(self, room: dict, ideas: list):
        self.RoomName.destroy()
        for l in self.evaluate:
            for var in l:
                var.set(False)

        for l in self.checkbuttons:
            for checkbutton in l:
                checkbutton.destroy()

        self.table.destroy()

        self.RoomName = None
        self.checkbuttons = [[] for _ in range(6)]
        self.table = None

        self.setup(room, ideas)

class RankingFrame(tk.Frame):
    def __init__(self, window: tk.Tk):
        super().__init__(window)
        self.RoomName = None
        self.exitButton = None
        self.rankingBoard = None

    def setup(self, room: dict, ideas: list):
        room_name = room["room_name"]
        self.RoomName =tk.Label(self, text=room_name, relief=tk.GROOVE)
        self.RoomName.pack()
        column = ("place", "idea", "score", "author")
        self.rankingBoard = ttk.Treeview(self, columns=column)
        self.rankingBoard.column('place',anchor='center', width=50)
        self.rankingBoard.column('idea', anchor='w', width=200)
        self.rankingBoard.column('score',anchor='center', width=80)
        self.rankingBoard.column('author', anchor='center', width=80)

        self.rankingBoard.heading('place',text='Place', anchor='center')
        self.rankingBoard.heading('idea', text='Idea',anchor='center')
        self.rankingBoard.heading('score', text='Score', anchor='center')
        self.rankingBoard.heading('author',text='Author', anchor='center')

        for i, idea in enumerate(ideas):
            self.rankingBoard.insert(
                parent='', index='end', iid=i ,values=(i+1, idea["idea"], idea["num_eval"], "未実装")
                )
            
        self.rankingBoard.pack()
        self.exitButton = tk.Button(self, text="終了", relief=tk.RIDGE)
        #self.exitButton.pack()