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

