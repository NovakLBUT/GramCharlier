import numpy as np
from scipy import stats as sc
import pandas as pd


class GramCharlier(object):
    def __init__(self):

        self.moments = None
        self.alpha = None
        self.beta = None
        self.gamma = None

    def eval_invcdf(self, file):
        df = pd.read_csv(file, sep=';', header=0)
        probability = df.to_numpy()
        sample = np.zeros(len(probability))

        for i in range(len(probability)):
            sample[i] = (self.bisect(probability[i, 0]))

        res = np.zeros((len(probability), 2))
        res[:, 0] = probability[:, 0]
        res[:, 1] = sample
        res = pd.DataFrame(res)
        res.to_csv(file.replace('.csv', '_sample.csv'), header=['p', 'X'], sep=';')

    def eval_distrib(self, file):
        df = pd.read_csv(file, sep=';', header=0)
        points = df.to_numpy()
        evalpdf = self.pdf(points)
        evalcdf = self.cdf(points)
        res = np.zeros((len(points), 3))
        res[:, 0] = points[:, 0]
        res[:, 1] = evalpdf[:, 0]
        res[:, 2] = evalcdf[:, 0]
        distribs = pd.DataFrame(res)
        distribs.to_csv(file.replace('.csv', '_distrib.csv'), header=['X', 'pdf', 'cdf'], sep=';')

    def estimate_quantile(self, coeffs):
        self.alpha = coeffs[0]
        self.beta = coeffs[1]
        self.gamma = coeffs[2]
        self.bisect()

    def bisect(self, p=None, eps=0.00001):

        def samesign(a, b):
            return a * b > 0

        low = self.moments[0] - 5 * np.sqrt(self.moments[1])
        high = self.moments[0] + 5 * np.sqrt(self.moments[1])
        diff = 1

        assert not samesign(self.inv_cdf(low, p), self.inv_cdf(high, p))
        midpoint = (low + high) / 2.0
        while diff > eps:
            midpoint = (low + high) / 2.0
            low_p = self.inv_cdf(low, p)
            mid_p = self.inv_cdf(midpoint, p)
            diff = np.abs(mid_p)

            if samesign(low_p, mid_p):
                low = midpoint
            else:
                high = midpoint

        if p is None:
            self.quantile = midpoint / self.gamma
        else:
            return midpoint

    def estimate_moments(self, file):
        df = pd.read_csv(file, sep=';', header=0)
        self.samples = df.to_numpy()
        mean = np.mean(self.samples)
        variance = np.var(self.samples)
        skewness = sc.skew(self.samples)[0]
        kurt = sc.kurtosis(self.samples)[0] + 3
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

    def inv_cdf(self, x, p):

        GC = self.cdf(x)

        if p is None:
            quantile_gauss = -self.alpha * self.beta
        else:
            quantile_gauss = sc.norm.ppf(p)

        target_p = sc.norm.cdf(quantile_gauss)

        if GC < 0:
            GC = 0
        elif GC > 1:
            GC = 1

        return target_p - GC
