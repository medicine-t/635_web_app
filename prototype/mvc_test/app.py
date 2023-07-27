from controllers import TestController
import tkinter as tk

window = tk.Tk()
window.geometry("500x500")
c = TestController(window=window)
c.setup()

window.mainloop()