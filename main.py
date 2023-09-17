import tkinter as tk
from gccore import GramCharlier
from gcview import GCView
from gccontroller import GCController
import os


if __name__ == "__main__":
    basedir = os.path.dirname(__file__)

    root = tk.Tk()
    root.iconbitmap("GC.ico")
    model = GramCharlier()
    view = GCView(root, None)
    controller = GCController(model, view)
    view.controller = controller

    root.mainloop()
