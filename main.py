import tkinter as tk
from gccore import GramCharlier
from gcview import GCView
from gccontroller import GCController

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(pady=15, padx=15)
    root.title("Gram-Charlier Expansion")
    root.geometry("800x500")

    root.configure(background='white')

    model = GramCharlier()
    view = GCView(root, None)
    controller = GCController(model, view)
    view.controller = controller
    root.mainloop()