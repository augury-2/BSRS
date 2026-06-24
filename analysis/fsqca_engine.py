"""
fsqca_engine.py
A from-scratch fuzzy-set Qualitative Comparative Analysis (fsQCA) toolkit
following Ragin (2008), Fiss (2011), and Pappas & Woodside (2021).

Implements:
  - direct-method calibration (full-in / crossover / full-out anchors)
  - set-theoretic consistency, coverage, PRI
  - analysis of necessary conditions
  - truth table construction (frequency, raw & PRI consistency)
  - Quine-McCluskey minimization -> prime implicants
  - complex (conservative), parsimonious, and intermediate solutions
  - solution & configuration coverage/consistency
  - Fiss core (parsimonious ∩ intermediate) vs peripheral notation
"""
import itertools
import numpy as np
import pandas as pd


# ---------------- calibration ----------------
def calibrate(x, full_in, crossover, full_out):
    """Ragin's direct method of calibration -> fuzzy membership in [0,1]."""
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    # target log-odds at anchors (Ragin uses 0.95 / 0.5 / 0.05 -> ~+/-3)
    LO = np.log(0.95 / 0.05)  # ~2.944
    above = x >= crossover
    # scalars (avoid divide-by-zero)
    up = (full_in - crossover) if (full_in - crossover) != 0 else 1e-9
    dn = (crossover - full_out) if (crossover - full_out) != 0 else 1e-9
    dev = x - crossover
    log_odds = np.where(above, dev * (LO / up), dev * (LO / dn))
    out = np.exp(log_odds) / (1 + np.exp(log_odds))
    # clip to (0,1); nudge exact 0.5 away to keep cases in analysis
    out = np.clip(out, 1e-6, 1 - 1e-6)
    out[np.isclose(out, 0.5)] = 0.5 + 1e-4
    return out


# ---------------- set measures ----------------
def consistency_suff(X, Y):
    """Sufficiency consistency: X is subset of Y."""
    return np.sum(np.minimum(X, Y)) / np.sum(X)


def coverage_suff(X, Y):
    return np.sum(np.minimum(X, Y)) / np.sum(Y)


def pri_consistency(X, Y):
    minXY = np.minimum(X, Y)
    minXnY = np.minimum(X, 1 - Y)
    num = np.sum(minXY) - np.sum(np.minimum(minXY, minXnY))
    den = np.sum(X) - np.sum(np.minimum(minXY, minXnY))
    return num / den if den > 0 else np.nan


def consistency_nec(X, Y):
    """Necessity consistency: Y is subset of X."""
    return np.sum(np.minimum(X, Y)) / np.sum(Y)


def coverage_nec(X, Y):
    return np.sum(np.minimum(X, Y)) / np.sum(X)


# ---------------- necessity ----------------
def necessity_analysis(cal, outcome_name, condition_names):
    Y = cal[outcome_name].values
    notY = 1 - Y
    rows = []
    for cond in condition_names:
        x = cal[cond].values
        for label, vec in [(cond, x), ("~" + cond, 1 - x)]:
            rows.append({
                "Condition": label,
                "Outcome": "BSUC",
                "Consistency": consistency_nec(vec, Y),
                "Coverage": coverage_nec(vec, Y),
            })
    nec = pd.DataFrame(rows)
    # also for negated outcome
    rows2 = []
    for cond in condition_names:
        x = cal[cond].values
        for label, vec in [(cond, x), ("~" + cond, 1 - x)]:
            rows2.append({
                "Condition": label,
                "Outcome": "~BSUC",
                "Consistency": consistency_nec(vec, notY),
                "Coverage": coverage_nec(vec, notY),
            })
    nec_neg = pd.DataFrame(rows2)
    return nec, nec_neg


# ---------------- truth table ----------------
def truth_table(cal, outcome_name, condition_names,
                freq_cutoff=1, cons_cutoff=0.80, pri_cutoff=0.70):
    Y = cal[outcome_name].values
    k = len(condition_names)
    corners = list(itertools.product([1, 0], repeat=k))  # 1=present,0=absent
    n = len(Y)
    rows = []
    # membership of each case in each corner
    for corner in corners:
        memb = np.ones(n)
        for ci, present in enumerate(corner):
            x = cal[condition_names[ci]].values
            memb = np.minimum(memb, x if present else 1 - x)
        # cases belonging to this corner: membership > 0.5
        in_corner = memb > 0.5
        num = int(in_corner.sum())
        raw_cons = consistency_suff(memb, Y) if memb.sum() > 0 else np.nan
        pri = pri_consistency(memb, Y) if memb.sum() > 0 else np.nan
        rows.append({
            **{condition_names[i]: corner[i] for i in range(k)},
            "n_cases": num,
            "raw_consistency": raw_cons,
            "PRI": pri,
        })
    tt = pd.DataFrame(rows)
    # outcome coding
    tt["OUT"] = ((tt["n_cases"] >= freq_cutoff) &
                 (tt["raw_consistency"] >= cons_cutoff) &
                 (tt["PRI"] >= pri_cutoff)).astype(int)
    # rows below frequency cutoff are remainders (OUT = '-')
    tt["status"] = np.where(tt["n_cases"] < freq_cutoff, "remainder",
                            np.where(tt["OUT"] == 1, "sufficient", "not_sufficient"))
    return tt, corners


# ---------------- Quine-McCluskey minimization ----------------
def _covers(implicant, minterm):
    """implicant: tuple over {0,1,'-'}; minterm tuple over {0,1}."""
    return all(im == "-" or im == mt for im, mt in zip(implicant, minterm))


def _combine(a, b):
    """Combine two implicants differing in exactly one literal."""
    diff = 0
    res = []
    for x, y in zip(a, b):
        if x != y:
            diff += 1
            res.append("-")
        else:
            res.append(x)
    return tuple(res) if diff == 1 else None


def quine_mccluskey(minterms, dont_cares):
    """Return list of prime implicants (tuples over {0,1,'-'}) covering minterms,
    using minterms+dont_cares as the ON-set available for combination."""
    terms = set(minterms) | set(dont_cares)
    if not terms:
        return []
    groups = [set(t) for t in [terms]][0]
    current = set(terms)
    prime = set()
    while True:
        combined_any = False
        used = set()
        nxt = set()
        cur_list = list(current)
        for i in range(len(cur_list)):
            for j in range(i + 1, len(cur_list)):
                c = _combine(cur_list[i], cur_list[j])
                if c is not None:
                    nxt.add(c)
                    used.add(cur_list[i])
                    used.add(cur_list[j])
                    combined_any = True
        for t in current:
            if t not in used:
                prime.add(t)
        if not combined_any:
            break
        current = nxt
    # keep only primes that cover at least one real minterm
    primes = [p for p in prime if any(_covers(p, m) for m in minterms)]
    # Petrick / greedy set cover to get essential + minimal cover
    chosen = _minimal_cover(primes, minterms)
    return chosen


def _minimal_cover(primes, minterms):
    minterms = list(minterms)
    chosen = []
    remaining = set(minterms)
    # essential prime implicants
    while remaining:
        # coverage count
        cover_map = {p: [m for m in remaining if _covers(p, m)] for p in primes}
        # find essential: a minterm covered by only one prime
        essential = None
        for m in remaining:
            covering = [p for p in primes if _covers(p, m)]
            if len(covering) == 1:
                essential = covering[0]
                break
        if essential is None:
            # greedy: pick prime covering most remaining
            essential = max(primes, key=lambda p: len(cover_map[p]))
        chosen.append(essential)
        for m in cover_map[essential]:
            remaining.discard(m)
        primes = [p for p in primes if p != essential]
        if not primes and remaining:
            break
    return chosen


# ---------------- solution assembly ----------------
def implicant_to_expr(impl, condition_names):
    parts = []
    for val, name in zip(impl, condition_names):
        if val == 1:
            parts.append(name)
        elif val == 0:
            parts.append("~" + name)
    return " * ".join(parts) if parts else "(empty)"


def config_membership(impl, cal, condition_names):
    """Fuzzy membership of each case in a configuration (AND of literals)."""
    n = len(cal)
    memb = np.ones(n)
    for val, name in zip(impl, condition_names):
        x = cal[name].values
        if val == 1:
            memb = np.minimum(memb, x)
        elif val == 0:
            memb = np.minimum(memb, 1 - x)
    return memb


def solution_metrics(implicants, cal, condition_names, outcome_name):
    """Raw coverage, unique coverage, consistency per configuration + solution."""
    Y = cal[outcome_name].values
    membs = [config_membership(im, cal, condition_names) for im in implicants]
    rows = []
    for idx, im in enumerate(implicants):
        m = membs[idx]
        raw_cov = coverage_suff(m, Y)
        cons = consistency_suff(m, Y)
        # unique coverage: contribution beyond all other terms
        others = [membs[j] for j in range(len(membs)) if j != idx]
        if others:
            other_max = np.maximum.reduce(others)
        else:
            other_max = np.zeros_like(m)
        uniq = (np.sum(np.minimum(m, Y)) -
                np.sum(np.minimum(np.minimum(m, other_max), Y))) / np.sum(Y)
        rows.append({
            "Configuration": implicant_to_expr(im, condition_names),
            "raw_coverage": raw_cov,
            "unique_coverage": uniq,
            "consistency": cons,
        })
    df = pd.DataFrame(rows)
    # overall solution
    sol_memb = np.maximum.reduce(membs) if membs else np.zeros(len(Y))
    sol_cov = coverage_suff(sol_memb, Y)
    sol_cons = consistency_suff(sol_memb, Y)
    return df, sol_cov, sol_cons
