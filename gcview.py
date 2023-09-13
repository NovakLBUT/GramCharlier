import tkinter as tk
import sys
import os
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


class Toolbar(NavigationToolbar2Tk):

    def set_message(self, s):
        pass


class MyMenu(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        fileMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Main", underline=0, menu=fileMenu)
        fileMenu.add_command(label="About", underline=1)
        fileMenu.add_command(label="Restart", underline=1, command=self.restart_program)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=1, command=parent.destroy)
        parent.config(menu=self)

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)


class GCView:

    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.config_root()
        self.create_widgets()

    def config_root(self):
        self.root.title("Gram-Charlier Expansion")
        self.root.geometry("800x500")
        self.root.configure(background='white', pady=15, padx=15)

    def create_widgets(self):
        self.left_frame = tk.Frame(width=400, height=500, bg='white')
        self.left_frame.pack(side='left', fill='both', padx=10, pady=5, expand=True)
        self.right_frame = tk.Frame(width=400, height=500, bg='white')
        self.right_frame.pack(side='right', fill='both', padx=10, pady=5, expand=True)
        self.button_csv = tk.Button(self.left_frame, text='Load .csv', command=self.load_csv)
        self.button_csv.pack(side=tk.TOP, padx=10, pady=5, anchor=tk.NW)

        self.labels_bar = tk.Frame(self.left_frame, width=200, height=30, bg='white')
        self.labels_bar.pack(side=tk.TOP, padx=10, pady=5, anchor=tk.NW)
        self.mean_label = tk.Label(self.labels_bar, text='Mean', bg='white')
        self.mean_label.pack(side=tk.LEFT, padx=5)
        self.variance_label = tk.Label(self.labels_bar, text='Variance', bg='white')
        self.variance_label.pack(side=tk.LEFT, padx=5)
        self.skew_label = tk.Label(self.labels_bar, text='Skewness', bg='white')
        self.skew_label.pack(side=tk.LEFT, padx=5)
        self.kurt_label = tk.Label(self.labels_bar, text='Kurtosis', bg='white')
        self.kurt_label.pack(side=tk.LEFT, padx=5)

        self.moments_bar = tk.Frame(self.left_frame, width=200, height=30, bg='white')
        self.moments_bar.pack(side=tk.TOP, padx=5, pady=0, anchor=tk.NW)
        self.text_box_mean = tk.Entry(self.moments_bar, width=7)
        self.text_box_mean.pack(side=tk.LEFT, padx=5)
        self.text_box_variance = tk.Entry(self.moments_bar, width=7)
        self.text_box_variance.pack(side=tk.LEFT, padx=5)
        self.text_box_skew = tk.Entry(self.moments_bar, width=7)
        self.text_box_skew.pack(side=tk.LEFT, padx=10)
        self.text_box_kurt = tk.Entry(self.moments_bar, width=7)
        self.text_box_kurt.pack(side=tk.LEFT, padx=4)

        self.labels_bar2 = tk.Frame(self.left_frame, width=200, height=30, bg='white')
        self.labels_bar2.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.alpha_label = tk.Label(self.labels_bar2, text='alpha', bg='white')
        self.alpha_label.pack(side=tk.LEFT, padx=5)
        self.beta_label = tk.Label(self.labels_bar2, text='beta', bg='white')
        self.beta_label.pack(side=tk.LEFT, padx=15)
        self.gamma_label = tk.Label(self.labels_bar2, text='gamma', bg='white')
        self.gamma_label.pack(side=tk.LEFT, padx=15)
        self.quantile_label = tk.Label(self.labels_bar2, text='value', bg='white')
        self.quantile_label.pack(side=tk.LEFT, padx=5)

        self.semiprob_bar = tk.Frame(self.left_frame, width=200, height=30, bg='white')
        self.semiprob_bar.pack(side=tk.TOP, padx=5, pady=0, anchor=tk.NW)
        self.text_box_alpha = tk.Entry(self.semiprob_bar, width=7)
        self.text_box_alpha.pack(side=tk.LEFT, padx=5)
        self.text_box_beta = tk.Entry(self.semiprob_bar, width=7)
        self.text_box_beta.pack(side=tk.LEFT, padx=5)
        self.text_box_gamma = tk.Entry(self.semiprob_bar, width=7)
        self.text_box_gamma.pack(side=tk.LEFT, padx=10)
        self.text_box_quantile = tk.Entry(self.semiprob_bar, width=7)
        self.text_box_quantile.pack(side=tk.LEFT, padx=4)

        self.postprocess_bar = tk.Frame(self.left_frame, width=200, height=30, bg='white')
        self.postprocess_bar.pack(side=tk.TOP, padx=5, pady=25, anchor=tk.NW)
        self.button_recalc = tk.Button(self.postprocess_bar, text='Recalculate', command=self.recalculate)
        self.button_recalc.pack(side=tk.LEFT, padx=20, pady=5, anchor=tk.NW)
        self.button_evaluate = tk.Button(self.postprocess_bar, text='Evaluate .csv', command=self.load_csv)
        self.button_evaluate.pack(side=tk.RIGHT, padx=20, pady=5, anchor=tk.NW)

        self.menubar = MyMenu(self.root)

    def plot_results(self, fig):
        self.canvasmaster = tk.Canvas(self.right_frame, bg='white')
        self.canvasmaster.pack()
        self.canvas = FigureCanvasTkAgg(fig, self.canvasmaster)
        self.canvas.draw()

        self.frametoolbar = tk.Frame(self.right_frame)
        self.toolbar = Toolbar(self.canvas, self.frametoolbar)

        for button in self.toolbar.winfo_children():
            button.config(background='white')
        self.toolbar.config(background='white')
        self.toolbar.update()

        self.canvas.get_tk_widget().pack(side=tk.TOP, anchor=tk.NE)
        self.frametoolbar.pack(side=tk.BOTTOM, anchor=tk.SE)

        self.button_tex = tk.Button(self.right_frame, text="LaTeX export", background='white',
                                    command=lambda: self.controller.plot(Latex=True))
        self.button_tex.pack(side=tk.BOTTOM, anchor=tk.SE)

    def load_csv(self):
        csv_file_path = askopenfilename()
        self.controller.process_input(csv_file_path)

    def recalculate(self):
        self.controller.recalculateGC()
