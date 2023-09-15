
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk


class GCController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def clearplot(self):
        for child in self.view.right_frame.winfo_children():
            child.destroy()

    def evaluate_inverse(self, csv_file):
        self.model.eval_invcdf(csv_file)

    def evaluate_distrib(self, csv_file):
        self.model.eval_distrib(csv_file)

    def process_input(self, csv_file):
        self.model.estimate_moments(csv_file)
        self.clearplot()
        self.plot()

        i = 0
        for child in self.view.moments_bar.winfo_children():

            if type(child) == tk.Entry:
                child.delete(0, tk.END)
                child.insert(tk.END, '{}'.format(self.model.moments[i]))
                i = i + 1

    def extractmoments(self):
        i = 0
        extractedmoments = []
        for child in self.view.moments_bar.winfo_children():
            if type(child) == tk.Entry:
                extractedmoments.append(float(child.get()))
                i = i + 1

        self.model.moments = extractedmoments

    def extractquantile(self):
        i = 0
        quantiledata = []
        for child in self.view.semiprob_bar.winfo_children():
            if type(child) == tk.Entry:
                try:
                    quantiledata.append(float(child.get()))
                except ValueError:
                    break

                i = i + 1

        self.model.estimate_quantile(quantiledata)
        self.view.text_box_quantile.delete(0, tk.END)
        self.view.text_box_quantile.insert(tk.END, '{}'.format(self.model.quantile))

    def checkmomemnts(self):
        i = 0
        for child in self.view.moments_bar.winfo_children():
            if type(child) == tk.Entry:
                if len(child.get()) > 0:
                    i = i + 1
        if i == 4:
            return True
        else:
            return False

    def checksemiprob(self):
        i = 0
        input_check = np.zeros(4)
        for child in self.view.semiprob_bar.winfo_children():
            if type(child) == tk.Entry:
                if len(child.get()) > 0:
                    if float(child.get()) != 0:
                        input_check[i] = 1
            i = i + 1

        if input_check[0] == 1 and input_check[1] == 1:
            if input_check[2] == 0:
                self.view.text_box_gamma.delete(0, tk.END)
                self.view.text_box_gamma.insert(tk.END, '1')

            return True
        else:
            return False

    def recalculateGC(self):
        if self.checkmomemnts():
            self.extractmoments()

            if self.checksemiprob():
                self.extractquantile()

        self.clearplot()
        self.plot()

    def plot(self, Latex=False, n_bins=None):
        if Latex:
            plt.rcParams['axes.linewidth'] = 0.5
            plt.rcParams['text.usetex'] = True
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
            self.clearplot()

        hist = False
        quanntile = False
        if hasattr(self.model, 'samples'):
            n_samples = len(self.model.samples)
            if n_bins is None:
                if n_samples > 500:
                    n_bins = int(n_samples / 50)
                elif n_samples > 100:
                    n_bins = 20
            hist = True

        if hasattr(self.model, 'quantile'):
            quanntile = True

        fig, ax = plt.subplots(2, 1, figsize=(4.5, 4))
        mu = self.model.moments[0]

        std = np.sqrt(self.model.moments[1])
        x = np.arange(mu - 4 * std, mu + 4 * std, 8 * std / 1000)
        f = self.model.pdf(x)

        if hist:
            ax[0].hist(self.model.samples, n_bins, rwidth=0.6, color='black', density=True, alpha=0.6,
                       edgecolor='black', linewidth=1.2, label='Empirical')

        ax[0].plot(x, f, color='red', label='Gram-Charlier Expansion')

        ymin, ymax = ax[0].get_ylim()
        if quanntile:
            ax[0].scatter(self.model.quantile, ymax / 50, s=50, color='green')
            ax[0].text(self.model.quantile, ymax / 7, r'$X_d$ = {:#.3g}'.format(self.model.quantile), rotation=90,
                       va='bottom',
                       ha='center', color='green')

        ax[0].set_ylabel('PDF [-]')
        ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), ncol=2)
        ax[1].set_ylim(0, 1.1)

        if hist:
            n, bins, patches = ax[1].hist(self.model.samples, n_bins, color='black', density=True, histtype='step',
                                          cumulative=True)

        if quanntile:
            ax[1].scatter(self.model.quantile, 0.01, s=50, color='green')
            ax[1].text(self.model.quantile, 0.1, r'$X_d$ = {:#.3g}'.format(self.model.quantile), rotation=90,
                       va='bottom',
                       ha='center', color='green')

        F = self.model.cdf(x)
        ax[1].plot(x, F, color='red')
        ax[1].set_ylabel('CDF [-]')
        ax[1].set_xlabel('Quantity of interest')
        fig.tight_layout()
        self.view.plot_results(fig)
