import tkinter as tk
from gccore import GramCharlier
from gcview import GCView
from gccontroller import GCController

if __name__ == "__main__":
    root = tk.Tk()


    model = GramCharlier()
    view = GCView(root, None)
    controller = GCController(model, view)
    view.controller = controller



    root.mainloop()