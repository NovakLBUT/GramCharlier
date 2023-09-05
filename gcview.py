import tkinter as tk
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

class Toolbar(NavigationToolbar2Tk):

    def set_message(self, s):
        pass

class GCView:

    def __init__(self, root, controller):
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.button=tk.Button(text='Load .csv', command=self.load_csv)
        self.button.pack(side=tk.TOP, anchor=tk.NW)

    def plot_results(self, fig):
        self.frametoolbar = tk.Frame()
        self.canvas=FigureCanvasTkAgg(fig)
        self.canvas.draw()
        # creating the Matplotlib toolbar
        self.toolbar = Toolbar(self.canvas, self.frametoolbar)
        for button in self.toolbar.winfo_children():
            button.config(background='white')
        self.toolbar.config(background='white')
        self.toolbar.update()

        self.canvas.get_tk_widget().pack(side=tk.TOP, anchor=tk.NE)

        self.frametoolbar.pack(side=tk.BOTTOM, anchor=tk.SE)
    def load_csv(self):
        csv_file_path =askopenfilename()
        self.controller.process_input(csv_file_path)




