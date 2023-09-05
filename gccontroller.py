# import pandas as pd
# import os
# import re

# from itertools import islice

from scipy import stats as sc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from  matplotlib import colors
import gccore
import tkinter as tk
import csv
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
# test=GC_Expansion.GramCharlier([0,1,2,4])
# print(test.pdf(0))






class GCController:
    def __init__(self,model,view):
        self.model=model
        self.view=view

    def process_input(self,csv_file):
        self.model.estimate_moments(csv_file)
        self.plot()

    def plot(self,Latex=False,n_bins=None):

        if Latex==True:
            plt.rcParams['axes.linewidth'] = 0.5
            plt.rcParams['text.usetex'] = True
            # plt.rc('text.latex', preamble=r'\usepackage[bitstream-charter]{mathdesign}')
            plt.rcParams['font.size'] = 10
            plt.rcParams['xtick.major.width'] = 0.5
            plt.rcParams['ytick.major.width'] = 0.5
            # Times, Palatino, New Century Schoolbook, Bookman, Computer Modern Roman
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})

            import matplotlib

            matplotlib.use('pgf')
            plt.rcParams["pgf.texsystem"] = "pdflatex"
            plt.rcParams["pgf.rcfonts"] = False

            preamble = r'''\usepackage[utf8]{inputenc} %unicode support
                   \usepackage[czech]{babel}
                   \usepackage[T1]{fontenc}
                   \DeclareMathAlphabet{\pazocal}{OMS}{zplm}{m}{n}
                   \usepackage{calrsfs}
                   \usepackage{amsmath}
                   \usepackage{bm}
                   \usepackage[bitstream-charter]{mathdesign}
                   '''
            plt.rc('text.latex', preamble=preamble)
            plt.rcParams["pgf.preamble"] = preamble

        # the figure that will contain the plot
        # list of squares

        fig, ax = plt.subplots(2, 1, figsize=(4.5, 4))
        mu=self.model.moments[0]
        std=np.sqrt(self.model.moments[1])
        x=np.arange(mu-4*std, mu+4*std, 8*std/1000)

        f=self.model.pdf(x)

        n_samples=len(self.model.samples)
        if n_bins is None:
            if n_samples>500:
                n_bins=int(n_samples/50)
            elif n_samples>100:
                n_bins = 20

        ax[0].hist(self.model.samples, n_bins, rwidth=0.6, color='black', density=True, alpha=0.8, edgecolor='black', linewidth=1.2, label='Empirical')
        ax[0].plot(x, f, color='red', label='Gram-Charlier Expansion')
        ax[0].set_xlim(mu-4*std, mu+4*std)

        ax[0].set_ylabel('PDF [-]')
        ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), ncol=2)


        n, bins, patches=ax[1].hist(self.model.samples,n_bins, color='black', density = True, histtype = 'step', cumulative = True)
        F = self.model.cdf(bins)
        ax[1].plot(bins, F, color='red')
        ax[1].set_ylabel('CDF [-]')
        ax[1].set_xlabel('Quantity of interest')
        ax[1].set_xlim(mu - 4 * std, mu + 4 * std)
        fig.tight_layout()
        self.view.plot_results(fig)




