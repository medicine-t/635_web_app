import tkinter as tk

class FrameSwitcher:
    def __init__(self, parent):
        self.parent = parent
        self.current_frame: tk.Frame = None

    def switchTo(self, frame: tk.Frame):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame
        self.current_frame.pack()