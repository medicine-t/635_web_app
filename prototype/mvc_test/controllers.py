from models import *
from views import *
from frame_switcher import FrameSwitcher
import tkinter as tk

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
        self.model = Model()
        self.willCreate = False

    def _to_start(self):
        room_list = self.model.getRoomList()
        self.start_frame.setup(room_list)
        self.fr.switchTo(self.start_frame)
        self.start_frame.CreatRoom.bind("<Button-1>", self.create_room)
        for b in self.start_frame.RoomList:
            b.bind("<Button-1>", self.join_room)

    def join_room(self,event: tk.Event):
        button_text = event.widget["text"]
        room_name = button_text.split(".")[0]
        room_id = button_text.split(".")[1]
        self.willCreate = False
        self._to_registration(room_name, room_id)

    def create_room(self, event: tk.Event):
        room_name = self.start_frame.ToNameRoom.get()
        room_id = ""
        self.willCreate = True
        self._to_registration(room_name, room_id)

    def _to_registration(self, room_name: str, room_id: int):
        self.registration_frame.setup(room_name)
        self.fr.switchTo(self.registration_frame)
        self.registration_frame.Registration.bind("<Button-1>", self.registration)

    def registration(self, event: tk.Event):
        user_name = self.registration_frame.UserName.get()
        self.model.createUser(user_name)
        room_name = self.registration_frame.RoomName.cget("text")

        if self.willCreate:
            self.model.createRoom(room_name,self.model.user_id)

        self.model.registration(self.model.room_id,self.model.user_id)

        ## self._to~~
