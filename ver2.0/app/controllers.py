from models import *
from views import *
from frame_switcher import FrameSwitcher
import tkinter as tk
import datetime

class Controller:
    def __init__(self, window: tk.Tk) -> None:
        self.fr = FrameSwitcher(window)
        self.start_frame = StartFrame(window=window)
        self.registration_frame = RegistrationFrame(window=window)
        self.standby_frame = StandbyFrame(window=window)
        self.countdown_frame = CountdownFrame(window=window)
        self.writing_frame = WritingFrame(window=window)
        self.review_frame = ReviewFrame(window=window)
        self.ranking_frame = RankingFrame(window=window)
        self.model = Model()
        self.willCreate = False

        self.INTERVAL = 1 * 1000 #記入画面、評価画面のインターバル

    def _to_start(self, event: tk.Event):
        room_list = self.model.getRoomList()
        self.start_frame.setup(room_list)
        self.fr.switchTo(self.start_frame)
        self.start_frame.CreateRoom.bind("<Button-1>", self.create_room)
        for b in self.start_frame.RoomList:
            b.bind("<Button-1>", self.select_room)

    def select_room(self,event: tk.Event):
        button_text = event.widget["text"]
        self.model.room_name = button_text.split(".")[0]
        self.model.room_id = button_text.split(".")[1]
        self.willCreate = False
        self._to_registration()

    def create_room(self, event: tk.Event):
        self.model.room_name = self.start_frame.ToNameRoom.get()
        self.willCreate = True
        self._to_registration()

    def _to_registration(self):
        self.registration_frame.setup(self.model.room_name)
        self.fr.switchTo(self.registration_frame)
        self.registration_frame.Registration.bind("<Button-1>", self.join_room)

    def join_room(self, event: tk.Event):
        user_name = self.registration_frame.UserName.get()
        self.model.createUser(user_name)
        if self.willCreate:
            self.model.createRoom()

        self.model.joinRoom()
        self._to_standby()

    def _to_standby(self):
        room = self.model.getRoom()
        self.standby_frame.setup(room)
        self.standby_frame.Registration.bind("<Button-1>", self.start_room)
        self.fr.switchTo(self.standby_frame)
        self.standby_update()
    
    def standby_update(self):
        room = self.model.getRoom()
        self.standby_frame.update(room)
        if room["is_start"]:
            self._to_countdown()
        else:
            self.standby_frame.after(1000, self.standby_update)

    def start_room(self, event: tk.Event):
        res = self.model.startRoom()
        if res:
            self._to_countdown()

    def _to_countdown(self):
        room = self.model.getRoom()
        start_time = datetime.datetime.strptime(room["start_time"], '%Y-%m-%dT%H:%M:%S.%f') + datetime.timedelta(hours=9)
        diff = start_time - datetime.datetime.now()
        
        self.countdown_frame.setup(room, diff)
        self.fr.switchTo(self.countdown_frame)
        self.countdown_frame.after(diff.seconds*1000, self._to_writing)

    def _to_writing(self):
        room = self.model.getRoom()
        sheet = self.model.getSheet()
        self.writing_frame.setup(room, sheet["ideas"], room["phase_num"])
        self.fr.switchTo(self.writing_frame)
        self.writing_frame.after(self.INTERVAL, self.send_ideas)
    
    def send_ideas(self):
        ideaTextBox = self.writing_frame.ideaTextBox
        ideas = []
        for textbox in ideaTextBox:
            idea = textbox.get()
            if idea == "": 
                idea = "アイデア未記入"
            ideas.append(idea)
        sheet = self.model.editSheet(ideas)
        self.model.setSheet(sheet)
        self.writing_update()

    def writing_update(self):
        room = self.model.getRoom()
        if room["host_user"] == self.model.user_id:
            self.model.updateRoom()
        
        if room["phase_num"] >= 6:
            self._to_review()
        elif room["phase_num"] > self.model.phase_num:
            self.model.phase_num = room["phase_num"]
            sheet = self.model.getSheet()
            self.writing_frame.update(room, sheet["ideas"], room["phase_num"])
            self.writing_frame.after(self.INTERVAL, self.send_ideas)
        else:
            self.writing_frame.after(100, self.writing_update)
    
    def _to_review(self):
        room = self.model.getRoom()
        sheet = self.model.getSheet()
        self.review_frame.setup(room, sheet["ideas"])
        self.fr.switchTo(self.review_frame)
        self.review_frame.after(self.INTERVAL, self.send_evals)

    def send_evals(self):
        sheet = self.model.getSheet()
        evaluate = self.review_frame.evaluate
        for i, var_list in enumerate(evaluate):
            for j, var in enumerate(var_list):
                if var.get():
                    sheet["ideas"][i][j]["num_eval"] += 1
        
        self.model.setSheet(sheet)
        self.review_update()

    def review_update(self):
        room = self.model.getRoom()
        if room["host_user"] == self.model.user_id:
            self.model.updateRoom()

        if room["phase_num"] >= 12:
            self._to_ranking()
        elif room["phase_num"] > self.model.phase_num:
            self.model.phase_num = room["phase_num"]
            sheet = self.model.getSheet()
            self.review_frame.update(room, sheet["ideas"])
            self.review_frame.after(self.INTERVAL, self.send_evals)
        else:
            self.writing_frame.after(100, self.review_update)
        
    def _to_ranking(self):
        room = self.model.getRoom()
        sheets = self.model.getSheetList()
        ideas = self.totalling(sheets)
        self.ranking_frame.setup(room, ideas)
        self.fr.switchTo(self.ranking_frame)
        self.ranking_frame.exitButton.bind("<Button-1>", self._to_start)

    def totalling(self, sheets):
        ideas = []
        for sheet in sheets:
            for ideas_row in sheet["ideas"]:
                ideas.extend(ideas_row)
        
        ideas = sorted(ideas, key=lambda x: x['num_eval'], reverse=True)

        return ideas


    