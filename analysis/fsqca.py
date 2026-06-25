"""A self-contained fuzzy-set QCA toolkit.

Implements: direct calibration (Ragin, 2008), necessity analysis (consistency,
coverage, relevance of necessity), truth-table construction (frequency, raw and
PRI consistency), and Quine-McCluskey logical minimisation producing complex,
parsimonious and intermediate solutions with raw/unique coverage.
"""
import itertools
import numpy as np
import pandas as pd

LN95 = np.log(0.95 / 0.05)  # 2.9444


def calibrate(x, full_in, crossover, full_out):
    """Direct method of calibration (Ragin, 2008). Asymmetric log-odds anchoring.
    Returns fuzzy membership in [0,1] (clamped away from exact 0/1/0.5)."""
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    up = x >= crossover
    dn = ~up
    slope_up = LN95 / (full_in - crossover)
    slope_dn = LN95 / (crossover - full_out)
    lo = np.empty_like(x)
    lo[up] = (x[up] - crossover) * slope_up
    lo[dn] = (x[dn] - crossover) * slope_dn
    m = np.exp(lo) / (1 + np.exp(lo))
    # nudge exact crossover values off 0.5 (fsQCA convention)
    m = np.where(np.isclose(m, 0.5), 0.501, m)
    return np.clip(m, 1e-6, 1 - 1e-6)


def consistency_suf(cond, outcome):
    """Sufficiency consistency: sum(min(X,Y))/sum(X)."""
    return np.minimum(cond, outcome).sum() / cond.sum()


def pri_consistency(cond, outcome):
    minXY = np.minimum(cond, outcome).sum()
    minXnotY = np.minimum(cond, 1 - outcome).sum()
    denom = cond.sum() - minXnotY
    num = minXY - minXnotY
    return num / denom if denom > 0 else np.nan


def coverage_suf(cond, outcome):
    return np.minimum(cond, outcome).sum() / outcome.sum()


def necessity(cond, outcome):
    cons = np.minimum(cond, outcome).sum() / outcome.sum()
    cov = np.minimum(cond, outcome).sum() / cond.sum()
    # Relevance of Necessity (Schneider & Wagemann, 2012)
    ron = (1 - cond).sum() / (1 - np.minimum(cond, outcome)).sum()
    return cons, cov, ron


def build_truth_table(data, conditions, outcome, freq_cutoff=1, cons_cutoff=0.80):
    """data: DataFrame of calibrated memberships. Returns truth-table DataFrame."""
    k = len(conditions)
    Y = data[outcome].values
    rows = []
    for combo in itertools.product([1, 0], repeat=k):  # 1=present,0=absent
        # corner membership = min over conditions of (X if present else 1-X)
        mem = np.ones(len(data))
        for ci, present in zip(conditions, combo):
            xi = data[ci].values
            mem = np.minimum(mem, xi if present else 1 - xi)
        n_cases = int((mem > 0.5).sum())
        if mem.sum() == 0:
            cons = pri = 0.0
        else:
            cons = consistency_suf(mem, Y)
            pri = pri_consistency(mem, Y)
        rows.append(list(combo) + [n_cases, round(cons, 4), round(pri, 4)])
    tt = pd.DataFrame(rows, columns=list(conditions) + ["n_cases", "raw_consistency", "PRI"])
    tt = tt.sort_values("raw_consistency", ascending=False).reset_index(drop=True)
    # outcome assignment
    tt["outcome"] = ((tt["n_cases"] >= freq_cutoff) & (tt["raw_consistency"] >= cons_cutoff) & (tt["PRI"] >= 0.5)).astype(int)
    return tt


# --------- Quine-McCluskey minimisation ----------
def _combine(a, b):
    """Combine two implicants (tuples with values 0/1/None) differing in one literal."""
    diff = 0
    res = []
    for x, y in zip(a, b):
        if x == y:
            res.append(x)
        else:
            diff += 1
            res.append(None)
    return tuple(res) if diff == 1 else None


def qmc(minterms, dontcares, k):
    """Quine-McCluskey returning prime implicants covering minterms (using dontcares)."""
    terms = set(minterms) | set(dontcares)
    groups = [tuple((m >> (k - 1 - i)) & 1 for i in range(k)) for m in terms]
    current = set(groups)
    primes = set()
    while True:
        used = set()
        nxt = set()
        cur = list(current)
        for i in range(len(cur)):
            for j in range(i + 1, len(cur)):
                c = _combine(cur[i], cur[j])
                if c is not None:
                    nxt.add(c)
                    used.add(cur[i]); used.add(cur[j])
        for t in cur:
            if t not in used:
                primes.add(t)
        if not nxt:
            break
        current = nxt
    # prime implicant chart: cover only true minterms
    mt_tuples = [tuple((m >> (k - 1 - i)) & 1 for i in range(k)) for m in minterms]

    def covers(prime, mt):
        return all(p is None or p == v for p, v in zip(prime, mt))

    # greedy + essential cover
    primes = list(primes)
    uncovered = set(range(len(mt_tuples)))
    chosen = []
    # essential primes
    while uncovered:
        # find minterm covered by fewest primes
        cover_map = {idx: [p for p in primes if covers(p, mt_tuples[idx])] for idx in uncovered}
        # essential
        essential = [c[0] for idx, c in cover_map.items() if len(c) == 1]
        if essential:
            for p in set(essential):
                if p not in chosen:
                    chosen.append(p)
        else:
            # greedy: pick prime covering most uncovered
            best = max(primes, key=lambda p: sum(covers(p, mt_tuples[idx]) for idx in uncovered))
            chosen.append(best)
        uncovered = {idx for idx in uncovered if not any(covers(p, mt_tuples[idx]) for p in chosen)}
    return chosen


def implicant_to_expr(imp, conditions):
    parts = []
    for val, name in zip(imp, conditions):
        if val == 1:
            parts.append(name)
        elif val == 0:
            parts.append("~" + name)
    return " * ".join(parts) if parts else "(constant TRUE)"


def solution_coverage(data, implicants, conditions, outcome):
    """Compute raw & unique coverage and consistency for each implicant and overall."""
    Y = data[outcome].values

    def imp_membership(imp):
        mem = np.ones(len(data))
        for val, name in zip(imp, conditions):
            if val is None:
                continue
            xi = data[name].values
            mem = np.minimum(mem, xi if val == 1 else 1 - xi)
        return mem

    mems = [imp_membership(im) for im in implicants]
    sol = np.zeros(len(data))
    for m in mems:
        sol = np.maximum(sol, m)
    overall_cons = consistency_suf(sol, Y) if sol.sum() else np.nan
    overall_cov = coverage_suf(sol, Y) if Y.sum() else np.nan
    overall_pri = pri_consistency(sol, Y)
    rows = []
    for i, (im, m) in enumerate(zip(implicants, mems)):
        raw_cov = coverage_suf(m, Y)
        cons = consistency_suf(m, Y)
        pri = pri_consistency(m, Y)
        # unique coverage: coverage attributable only to this implicant
        others = np.zeros(len(data))
        for j, mm in enumerate(mems):
            if j != i:
                others = np.maximum(others, mm)
        unique = (np.minimum(m, Y).sum() - np.minimum(np.minimum(m, others), Y).sum()) / Y.sum()
        rows.append([implicant_to_expr(im, conditions), raw_cov, unique, cons, pri])
    cov_tbl = pd.DataFrame(rows, columns=["Configuration", "RawCoverage", "UniqueCoverage", "Consistency", "PRI"])
    return cov_tbl, dict(SolutionCoverage=overall_cov, SolutionConsistency=overall_cons, SolutionPRI=overall_pri)
