from models import *
from views import *
from frame_switcher import FrameSwitcher
import tkinter as tk

class Idea(BaseModel):
    idea : str = ""
    num_eval : int = 0

class TestController:
    def __init__(self, window: tk.Tk) -> None:
        self.fr = FrameSwitcher(window)
        self.frame = TestFrame(window=window)
        self.model = TestModel()
        
    def setup(self):
        self.frame.setup()
        self.frame.button.bind("<Button-1>", self.call_test)
        self.fr.switchTo(self.frame)
        self.frame.label.after(3000, self.waiting_method)

    def call_test(self, event: tk.Event):
        print(event.widget)
        button_text = event.widget["text"]
        self.model.test(button_text)

    def waiting_method(self):
        self.model.waitng_print()

class Controller:
    def __init__(self, window: tk.Tk) -> None:
        self.fr = FrameSwitcher(window)
        self.start_frame = StartFrame(window=window)
        self.registration_frame = RegistrationFrame(window=window)
        self.standby_frame = StandbyFrame(window=window)
        self.writing_frame = WritingFrame(window=window)
        self.review_frame = ReviewFrame(window=window)
        self.model = Model()
        self.willCreate = False

    def _to_start(self):
        room_list = self.model.getRoomList()
        self.start_frame.setup(room_list)
        self.fr.switchTo(self.start_frame)
        self.start_frame.CreateRoom.bind("<Button-1>", self.create_room)
        for b in self.start_frame.RoomList:
            b.bind("<Button-1>", self.join_room)

    def join_room(self,event: tk.Event):
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
        self.registration_frame.Registration.bind("<Button-1>", self.registration)

    def registration(self, event: tk.Event):
        user_name = self.registration_frame.UserName.cget("text")
        self.model.createUser(user_name)

        if self.willCreate:
            self.model.createRoom()

        self.model.registration()

        self._to_standby()

    def _to_standby(self):
        room = self.model.getRoom()
        self.standby_frame.setup(room)
        self.standby_update()
    
    def standby_update(self):
        room = self.model.getRoom()
        if room["is_start"] == True:
            print("room is start")
        self.standby_frame.after(1000, self.standby_update)

    def _to_writing(self):
        room = self.model.getRoom()
        sheet = self.model.getSheet()
        self.writing_frame.setup(room, sheet["ideas"], self.model.writing_count)
    
    def writing_update(self):
        sheet = self.model.getSheet()
        ideaTextBox = self.writing_frame.ideaTextBox
        ideas = []
        for textbox in ideaTextBox:
            idea = Idea()
            idea.idea = textbox.get()
            ideas.append(idea)
        sheet["ideas"] = ideas
        self.model.setSheet(sheet)
