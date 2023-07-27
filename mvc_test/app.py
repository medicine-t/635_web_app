from controllers import TestController
import tkinter as tk

window = tk.Tk()
window.geometry("500x500")
window["bg"] = "white"
c = TestController(window=window)
c.setup()

window.mainloop()