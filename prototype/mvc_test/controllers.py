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
        self.model = TestModel()

    def to_start(self):
        pass