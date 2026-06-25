"""A self-contained PLS-SEM estimator (Mode A reflective, path-weighting scheme).

Implements the Lohmoller/Wold partial least squares path-modelling algorithm:
  1. Standardise indicators.
  2. Initialise outer weights to 1 and form composite scores.
  3. Inner approximation (path-weighting scheme): sign of correlation for
     adjacent constructs.
  4. Outer approximation (Mode A): regress each indicator on the inner
     composite (i.e. correlation), giving updated outer weights.
  5. Re-scale composites to unit variance; iterate to convergence.
  6. Outer loadings = correlation(indicator, composite).
  7. Structural coefficients = OLS of each endogenous composite on its
     predecessors.

Only what is needed for this study is implemented, but it follows the standard
references (Hair et al., 2022; Henseler et al., 2009).
"""
import numpy as np
import pandas as pd


class PLSSEM:
    def __init__(self, constructs, paths, max_iter=500, tol=1e-9):
        self.constructs = {k: list(v) for k, v in constructs.items()}
        self.lv_names = list(constructs.keys())
        self.paths = list(paths)
        self.max_iter = max_iter
        self.tol = tol
        # adjacency (inner model): D[j,i]=1 if i predicts j or j predicts i
        n = len(self.lv_names)
        self.idx = {lv: k for k, lv in enumerate(self.lv_names)}
        self.adj = np.zeros((n, n))
        self.pred = {lv: [] for lv in self.lv_names}  # predecessors
        for a, b in self.paths:
            ia, ib = self.idx[a], self.idx[b]
            self.adj[ia, ib] = 1
            self.adj[ib, ia] = 1
            self.pred[b].append(a)

    def fit(self, df):
        self.indicators = [i for lv in self.lv_names for i in self.constructs[lv]]
        X = df[self.indicators].astype(float).values
        self.Xmean = X.mean(axis=0)
        self.Xstd = X.std(axis=0, ddof=1)
        Xs = (X - self.Xmean) / self.Xstd
        self.Xs = Xs
        N = Xs.shape[0]
        n = len(self.lv_names)

        # map indicator columns to each LV
        cols = {}
        c = 0
        for lv in self.lv_names:
            k = len(self.constructs[lv])
            cols[lv] = list(range(c, c + k))
            c += k
        self.cols = cols

        # init outer weights = 1
        w = {lv: np.ones(len(cols[lv])) for lv in self.lv_names}

        def scores(weights):
            Y = np.zeros((N, n))
            for j, lv in enumerate(self.lv_names):
                yc = Xs[:, cols[lv]] @ weights[lv]
                yc = (yc - yc.mean()) / yc.std(ddof=1)
                Y[:, j] = yc
            return Y

        Y = scores(w)
        for _ in range(self.max_iter):
            # inner approximation (path weighting / centroid hybrid -> use factor scheme: correlation)
            E = np.zeros((n, n))
            R = np.corrcoef(Y, rowvar=False)
            for i in range(n):
                for j in range(n):
                    if self.adj[i, j]:
                        E[i, j] = R[i, j]
            Z = Y @ E  # inner composite for each LV (column j uses neighbours)
            # rescale Z columns
            for j in range(n):
                s = Z[:, j].std(ddof=1)
                if s > 0:
                    Z[:, j] = (Z[:, j] - Z[:, j].mean()) / s
            # outer approximation Mode A: weight = cov(indicator, Z_lv)
            w_new = {}
            for j, lv in enumerate(self.lv_names):
                zc = Z[:, j]
                ws = np.array([np.cov(Xs[:, ci], zc, ddof=1)[0, 1] for ci in cols[lv]])
                w_new[lv] = ws
            Y_new = scores(w_new)
            diff = max(np.abs(np.abs(w_new[lv]) - np.abs(w[lv])).max() for lv in self.lv_names)
            w = w_new
            Y = Y_new
            if diff < self.tol:
                break

        self.weights = w
        self.scores_ = pd.DataFrame(Y, columns=self.lv_names)

        # ---- Stabilise the measurement solution -------------------------------
        # When constructs are near-orthogonal the iterated inner weights are
        # weakly identified. For reflective (Mode A) blocks the converged weights
        # are proportional to the loadings, so we recompute the final composite
        # scores with loading-proportional weights (scaled to unit variance) and
        # iterate the corr(indicator, composite) step to a fixed point per block.
        Yfix = np.zeros_like(Y)
        self._stable_w = {}
        for j, lv in enumerate(self.lv_names):
            Xi = Xs[:, cols[lv]]
            wl = np.ones(Xi.shape[1])
            for _ in range(200):
                comp = Xi @ wl
                comp = (comp - comp.mean()) / comp.std(ddof=1)
                new = np.array([np.corrcoef(Xi[:, k], comp)[0, 1] for k in range(Xi.shape[1])])
                if np.abs(new - wl).max() < 1e-10:
                    wl = new
                    break
                wl = new
            comp = Xi @ wl
            sc = comp.std(ddof=1)
            comp = (comp - comp.mean()) / sc
            # orient so loadings are positive on average
            if np.mean([np.corrcoef(Xi[:, k], comp)[0, 1] for k in range(Xi.shape[1])]) < 0:
                comp = -comp
                wl = -wl
            Yfix[:, j] = comp
            self._stable_w[lv] = wl / sc  # scaled so composite has unit variance
        Y = Yfix
        self.scores_ = pd.DataFrame(Y, columns=self.lv_names)

        # standardized outer weights (so composite has unit variance)
        self.outer_weights = {lv: self._stable_w[lv] for lv in self.lv_names}

        # outer loadings = corr(indicator, composite)
        load = {}
        cross = pd.DataFrame(index=self.indicators, columns=self.lv_names, dtype=float)
        for lv in self.lv_names:
            for k, ci in enumerate(cols[lv]):
                pass
        for ind_i, ind in enumerate(self.indicators):
            for lv in self.lv_names:
                cross.loc[ind, lv] = np.corrcoef(Xs[:, ind_i], Y[:, self.idx[lv]])[0, 1]
        self.cross_loadings = cross
        self.loadings = {}
        for lv in self.lv_names:
            self.loadings[lv] = cross.loc[self.constructs[lv], lv].values.astype(float)

        # structural coefficients (OLS on standardized composites)
        self.path_coef = {}
        self.r2 = {}
        self.r2_adj = {}
        self.residuals = {}
        self.fitted = {}
        for lv in self.lv_names:
            preds = self.pred[lv]
            if not preds:
                continue
            Xp = self.scores_[preds].values
            y = self.scores_[lv].values
            Xd = np.column_stack([np.ones(N), Xp])
            beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
            yhat = Xd @ beta
            resid = y - yhat
            ss_res = (resid ** 2).sum()
            ss_tot = ((y - y.mean()) ** 2).sum()
            r2 = 1 - ss_res / ss_tot
            p = len(preds)
            self.path_coef[lv] = dict(zip(preds, beta[1:]))
            self.r2[lv] = r2
            self.r2_adj[lv] = 1 - (1 - r2) * (N - 1) / (N - p - 1)
            self.residuals[lv] = resid
            self.fitted[lv] = yhat
        return self

    # ---- reliability / validity ----
    def reliability(self):
        rows = []
        for lv in self.lv_names:
            L = np.asarray(self.loadings[lv])
            k = len(L)
            Xi = self.Xs[:, self.cols[lv]]
            # Cronbach alpha
            tot = Xi.sum(axis=1)
            alpha = k / (k - 1) * (1 - Xi.var(axis=0, ddof=1).sum() / tot.var(ddof=1))
            # Composite reliability (rho_c)
            sl = L.sum() ** 2
            err = (1 - L ** 2).sum()
            cr = sl / (sl + err)
            ave = (L ** 2).mean()
            # rho_A (Dijkstra & Henseler, 2015). For a reflective block the Mode A
            # weights are proportional to the loadings; we scale them so the
            # composite has unit variance (w'Sw = 1), which stabilises the
            # estimate when constructs are near-orthogonal.
            S = np.corrcoef(Xi, rowvar=False)
            w = L.copy().astype(float)
            w = w / np.sqrt(w @ S @ w)
            ww = np.outer(w, w)
            off_S = S - np.diag(np.diag(S))
            off_ww = ww - np.diag(np.diag(ww))
            num = w @ off_S @ w
            den = w @ off_ww @ w
            rho_a = (w @ w) ** 2 * (num / den) if den != 0 else np.nan
            rows.append([lv, k, alpha, rho_a, cr, ave])
        return pd.DataFrame(rows, columns=["Construct", "Items", "CronbachAlpha", "rhoA", "CR", "AVE"]).set_index("Construct")

    def fornell_larcker(self):
        rel = self.reliability()
        corr = self.scores_.corr()
        FL = corr.copy()
        for lv in self.lv_names:
            FL.loc[lv, lv] = np.sqrt(rel.loc[lv, "AVE"])
        # lower triangle = correlations, diagonal = sqrt(AVE)
        return FL

    def htmt(self):
        names = self.lv_names
        H = pd.DataFrame(index=names, columns=names, dtype=float)
        S = np.corrcoef(self.Xs, rowvar=False)
        for a in range(len(names)):
            for b in range(len(names)):
                if a == b:
                    H.iloc[a, b] = np.nan
                    continue
                ca, cb = self.cols[names[a]], self.cols[names[b]]
                # heterotrait-heteromethod mean
                het = np.mean([abs(S[i, j]) for i in ca for j in cb])
                # monotrait within a
                def mono(cset):
                    vals = [abs(S[i, j]) for ii, i in enumerate(cset) for j in cset[ii+1:]]
                    return np.mean(vals)
                ma, mb = mono(ca), mono(cb)
                H.iloc[a, b] = het / np.sqrt(ma * mb)
        return H

    def full_collinearity_vif(self):
        """Kock (2015) full collinearity VIF using composite scores."""
        Z = self.scores_.values
        names = self.lv_names
        vifs = {}
        for j, lv in enumerate(names):
            y = Z[:, j]
            Xo = np.column_stack([np.ones(len(y))] + [Z[:, k] for k in range(len(names)) if k != j])
            beta, *_ = np.linalg.lstsq(Xo, y, rcond=None)
            yhat = Xo @ beta
            r2 = 1 - ((y - yhat) ** 2).sum() / ((y - y.mean()) ** 2).sum()
            vifs[lv] = 1 / (1 - r2) if r2 < 1 else np.inf
        return pd.Series(vifs, name="FullCollinearityVIF")

    def inner_vif(self):
        """VIF among predictors for each structural equation."""
        out = {}
        for lv in self.lv_names:
            preds = self.pred[lv]
            if len(preds) < 2:
                if len(preds) == 1:
                    out[lv] = {preds[0]: 1.0}
                continue
            d = {}
            for p in preds:
                others = [q for q in preds if q != p]
                y = self.scores_[p].values
                Xo = np.column_stack([np.ones(len(y))] + [self.scores_[q].values for q in others])
                beta, *_ = np.linalg.lstsq(Xo, y, rcond=None)
                yhat = Xo @ beta
                r2 = 1 - ((y - yhat) ** 2).sum() / ((y - y.mean()) ** 2).sum()
                d[p] = 1 / (1 - r2) if r2 < 1 else np.inf
            out[lv] = d
        return out

    def f_squared(self):
        """Effect size f2 for each structural path."""
        res = {}
        for lv in self.lv_names:
            preds = self.pred[lv]
            if not preds:
                continue
            y = self.scores_[lv].values
            full = self.r2[lv]
            for p in preds:
                others = [q for q in preds if q != p]
                if others:
                    Xo = np.column_stack([np.ones(len(y))] + [self.scores_[q].values for q in others])
                    beta, *_ = np.linalg.lstsq(Xo, y, rcond=None)
                    yhat = Xo @ beta
                    r2_excl = 1 - ((y - yhat) ** 2).sum() / ((y - y.mean()) ** 2).sum()
                else:
                    r2_excl = 0.0
                f2 = (full - r2_excl) / (1 - full) if full < 1 else np.nan
                res[(p, lv)] = f2
        return res

    def model_fit(self):
        """SRMR, d_ULS, d_G, NFI, RMS_theta on the indicator correlation matrix."""
        S = np.corrcoef(self.Xs, rowvar=False)  # observed
        # implied correlation matrix from loadings + LV correlations
        n_ind = len(self.indicators)
        Lambda = np.zeros((n_ind, len(self.lv_names)))
        r = 0
        for j, lv in enumerate(self.lv_names):
            for k in self.cols[lv]:
                Lambda[k, j] = self.loadings[lv][k - self.cols[lv][0]]
        Phi = self.scores_.corr().values
        Sigma = Lambda @ Phi @ Lambda.T
        # diagonal = 1 (standardized) ; off-diagonal blocks for same construct via loadings product
        for lv in self.lv_names:
            cc = self.cols[lv]
            for a in cc:
                for b in cc:
                    if a != b:
                        Sigma[a, b] = self.loadings[lv][a-cc[0]] * self.loadings[lv][b-cc[0]]
        np.fill_diagonal(Sigma, 1.0)
        iu = np.triu_indices(n_ind, 1)
        resid = S[iu] - Sigma[iu]
        srmr = np.sqrt((resid ** 2).mean())
        d_uls = (resid ** 2).sum()
        # geodesic distance
        eig_s = np.linalg.eigvalsh(np.linalg.solve(Sigma, S))
        eig_s = eig_s[eig_s > 0]
        d_g = 0.5 * (np.log(eig_s) ** 2).sum() if len(eig_s) else np.nan
        # NFI: 1 - chi/chi_null ; approximate with sums of squared residuals
        null_resid = S[iu]  # baseline = independence (Sigma=I)
        nfi = 1 - (resid ** 2).sum() / (null_resid ** 2).sum()
        # RMS_theta: rms of off-diagonal residual correlations of outer model residuals
        # approximate using indicator residual correlations after extracting composite
        E = self.Xs.copy()
        for lv in self.lv_names:
            yc = self.scores_[lv].values
            for k in self.cols[lv]:
                l = self.loadings[lv][k - self.cols[lv][0]]
                E[:, k] = self.Xs[:, k] - l * yc
        Re = np.corrcoef(E, rowvar=False)
        rms_theta = np.sqrt((Re[iu] ** 2).mean())
        return dict(SRMR=srmr, d_ULS=d_uls, d_G=d_g, NFI=nfi, RMS_theta=rms_theta)
