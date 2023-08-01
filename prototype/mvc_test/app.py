from controllers import Controller
import tkinter as tk

window = tk.Tk()
window.geometry("500x500")
c = Controller(window=window)
c._to_start(tk.Event())

window.mainloop()
