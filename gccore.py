import numpy as np
from scipy import stats as sc
import pandas as pd




class GramCharlier(object):
    def __init__(self):
        
        self.moments = None

    def estimate_moments(self, file):
        df = pd.read_csv(file, sep=';', header=0)
        self.samples = df.to_numpy()
        mean = np.mean(self.samples)
        variance = np.var(self.samples)
        skewness = sc.skew(self.samples)
        kurt = sc.kurtosis(self.samples) + 3
        self.moments = [mean, variance, skewness, kurt]
        
    def normalized_hermite(self, N):
        plist = [None] * N
        plist[0] = np.poly1d(1)
        for n in range(1, N):
            plist[n] = (-plist[n - 1].deriv() + np.poly1d([1, 0]) * plist[n - 1]) / np.sqrt(n)
        return plist

    def standardize_sample(self, x):
        s = (x - self.moments[0]) / np.sqrt(self.moments[1])
        return s

    def pdf(self, x):
        m1, m2, m3, m4 = self.moments
        GCexp = np.poly1d(1)
        s = self.standardize_sample(x)
        Hp = self.normalized_hermite(5)

        C3 = m3 / np.sqrt(6.0)
        C4 = (m4 - 3) / np.sqrt(24.0)

        GCexp = GCexp + C3 * Hp[3] + C4 * Hp[4]

        p = GCexp(s) * np.exp(-s * s / 2.0) / np.sqrt(2 * np.pi) / np.sqrt(m2)

        return p

    def cdf(self, x):
        m1, m2, m3, m4 = self.moments
        GCexp = np.poly1d(1)
        s = self.standardize_sample(x)
        Hp = self.normalized_hermite(5)

        C3 = -m3 / (np.sqrt(2) * 3)
        C4 = -(m4 - 3) / (np.sqrt(6) * 4)

        GCexp = GCexp + C3 * Hp[2] + C4 * Hp[3]
        p = sc.norm.cdf(s) + GCexp(s) * np.exp(-s * s / 2.0) / np.sqrt(2 * np.pi) / np.sqrt(m2) - np.exp(
            -s * s / 2.0) / np.sqrt(2 * np.pi) / np.sqrt(m2)
        return p