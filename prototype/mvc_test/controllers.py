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

    def _to_start(self):
        room_list = self.model.getRoomList()
        self.start_frame.setup(room_list)
        self.fr.switchTo(self.start_frame)
        self.start_frame.CreatRoom.bind("<Button-1>", self.creat_room)
        for b in self.start_frame.RoomList:
            b.bind("<Button-1>", self.join_room)

    def join_room(self,event: tk.Event):
        button_text = event.widget["text"]
        room_name = button_text.split(".")[1]
        room_name = self.model.getRoom()
        pass

    def create_room(self):
        room_name = self.start_frame.ToNameRoom.get()
        room_id = self.model.createRoom(room_name=room_name, user_id=user_id)
        self._to_registration()

    def _to_registration(self, room_id: str):
        pass