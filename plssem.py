"""
Lightweight PLS-SEM implementation (Mode A / reflective, path weighting scheme).
Implements the standard Wold/Lohmoller PLS algorithm, consistent with SmartPLS defaults.
"""
import numpy as np
import pandas as pd


def _standardize(X):
    return (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)


class PLSSEM:
    def __init__(self, data, measurement, structural, max_iter=500, tol=1e-9):
        """
        data: pandas DataFrame with indicator columns
        measurement: dict {construct: [indicator cols]} (all reflective, Mode A)
        structural: dict {endogenous_construct: [predecessor_constructs]}
        """
        self.constructs = list(measurement.keys())
        self.measurement = measurement
        self.structural = structural
        self.max_iter = max_iter
        self.tol = tol
        self.indicators = [i for c in self.constructs for i in measurement[c]]
        self.data = data[self.indicators].astype(float).reset_index(drop=True)
        self.n = self.data.shape[0]

        # adjacency matrix (symmetric, for inner weighting)
        self.adj = pd.DataFrame(0.0, index=self.constructs, columns=self.constructs)
        for endo, preds in structural.items():
            for p in preds:
                self.adj.loc[endo, p] = 1.0
                self.adj.loc[p, endo] = 1.0

    def fit(self, X=None):
        if X is None:
            X = self.data
        Xs = _standardize(X.values)
        col_index = {c: i for i, c in enumerate(X.columns)}
        # indicator blocks
        blocks = {c: [col_index[i] for i in self.measurement[c]] for c in self.constructs}

        # init outer weights = 1 for each indicator
        W = {c: np.ones(len(blocks[c])) for c in self.constructs}

        def composite_scores(W):
            Y = np.zeros((Xs.shape[0], len(self.constructs)))
            for j, c in enumerate(self.constructs):
                Xb = Xs[:, blocks[c]]
                y = Xb @ W[c]
                y = (y - y.mean()) / y.std(ddof=1)
                Y[:, j] = y
            return Y

        Y = composite_scores(W)

        for _ in range(self.max_iter):
            W_old = {c: W[c].copy() for c in self.constructs}
            # Inner approximation (path weighting scheme)
            E = np.zeros((len(self.constructs), len(self.constructs)))
            corr = np.corrcoef(Y, rowvar=False)
            for j, cj in enumerate(self.constructs):
                for k, ck in enumerate(self.constructs):
                    if self.adj.loc[cj, ck] == 1.0:
                        # successor (cj is endogenous, ck predictor): use regression coef
                        if ck in self.structural.get(cj, []):
                            # multiple regression of Yj on its predictors
                            preds = self.structural[cj]
                            idx = [self.constructs.index(p) for p in preds]
                            Xp = Y[:, idx]
                            beta, *_ = np.linalg.lstsq(Xp, Y[:, j], rcond=None)
                            E[k, j] = beta[preds.index(ck)]
                        else:
                            # cj is predecessor of ck: use correlation
                            E[k, j] = corr[j, k]
            Z = Y @ E  # inner composite for each construct (column)

            # Outer weights update (Mode A: correlation/regression of indicators on inner composite)
            for j, c in enumerate(self.constructs):
                Xb = Xs[:, blocks[c]]
                z = Z[:, j]
                z = (z - z.mean()) / z.std(ddof=1)
                # Mode A: w = cov(X, z); simple regression of each indicator on z
                w = (Xb.T @ z) / (Xs.shape[0] - 1)
                W[c] = w

            Y = composite_scores(W)

            diff = max(np.max(np.abs(np.abs(W[c]) - np.abs(W_old[c]))) for c in self.constructs)
            if diff < self.tol:
                break

        # Final composite scores
        self.scores = pd.DataFrame(Y, columns=self.constructs)
        self.weights = W

        # Loadings = correlation indicator vs construct score
        self.loadings = {}
        for c in self.constructs:
            self.loadings[c] = {}
            for i in self.measurement[c]:
                xi = Xs[:, col_index[i]]
                self.loadings[c][i] = np.corrcoef(xi, self.scores[c].values)[0, 1]

        # Path coefficients (standardized OLS per endogenous construct)
        self.paths = {}
        self.r2 = {}
        self.r2_adj = {}
        for endo, preds in self.structural.items():
            Xp = self.scores[preds].values
            y = self.scores[endo].values
            beta, *_ = np.linalg.lstsq(Xp, y, rcond=None)
            self.paths[endo] = dict(zip(preds, beta))
            yhat = Xp @ beta
            ss_res = np.sum((y - yhat) ** 2)
            ss_tot = np.sum((y - y.mean()) ** 2)
            r2 = 1 - ss_res / ss_tot
            self.r2[endo] = r2
            k = len(preds)
            self.r2_adj[endo] = 1 - (1 - r2) * (self.n - 1) / (self.n - k - 1)
        return self

    # ---- Reliability / validity metrics ----
    def reliability(self):
        out = {}
        Xs = _standardize(self.data.values)
        col_index = {c: i for i, c in enumerate(self.data.columns)}
        for c in self.constructs:
            items = self.measurement[c]
            L = np.array([self.loadings[c][i] for i in items])
            # Cronbach alpha
            sub = self.data[items].values
            kk = len(items)
            item_var = sub.var(axis=0, ddof=1).sum()
            total_var = sub.sum(axis=1).var(ddof=1)
            alpha = kk / (kk - 1) * (1 - item_var / total_var)
            # Composite reliability (rho_c)
            sumL = L.sum()
            sum_err = np.sum(1 - L ** 2)
            cr = sumL ** 2 / (sumL ** 2 + sum_err)
            # AVE
            ave = np.mean(L ** 2)
            out[c] = dict(alpha=alpha, CR=cr, AVE=ave, min_load=L.min(), max_load=L.max())
        return pd.DataFrame(out).T

    def htmt(self):
        # HTMT = mean(heterotrait-heteromethod corr) / geomean(mean(monotrait corr))
        absC = self.data.corr().abs()
        H = pd.DataFrame(index=self.constructs, columns=self.constructs, dtype=float)
        for a in self.constructs:
            for b in self.constructs:
                ia, ib = self.measurement[a], self.measurement[b]
                if a == b:
                    H.loc[a, b] = np.nan
                    continue
                hetero = absC.loc[ia, ib].values.mean()
                # monotrait avg (off-diagonal) for a
                def mono(items):
                    m = absC.loc[items, items].values
                    iu = np.triu_indices(len(items), k=1)
                    return m[iu].mean()
                mono_a = mono(ia)
                mono_b = mono(ib)
                H.loc[a, b] = hetero / np.sqrt(mono_a * mono_b)
        return H

    def construct_correlations(self):
        return self.scores.corr()

    def full_collinearity_vif(self):
        # regress each construct score on all other construct scores
        vifs = {}
        for c in self.constructs:
            others = [x for x in self.constructs if x != c]
            X = self.scores[others].values
            y = self.scores[c].values
            beta, *_ = np.linalg.lstsq(X, y, rcond=None)
            yhat = X @ beta
            ss_res = np.sum((y - yhat) ** 2)
            ss_tot = np.sum((y - y.mean()) ** 2)
            r2 = 1 - ss_res / ss_tot
            vifs[c] = 1 / (1 - r2)
        return pd.Series(vifs, name="VIF")

    def fornell_larcker(self):
        rel = self.reliability()
        C = self.construct_correlations().copy()
        for c in self.constructs:
            C.loc[c, c] = np.sqrt(rel.loc[c, "AVE"])
        return C
