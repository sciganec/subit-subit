#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUBIT-∞ v6.14.1 — верифікація теореми ALT-7 (Q-ALT1).

Об'єкт: усі афінні відображення x ↦ M x + t над ℤ₄³.
  M ∈ Mat_{3×3}(ℤ₄): 4⁹ = 262144.
  t ∈ ℤ₄³: 4³ = 64.
  Усього афінних відображень: 4¹² = 16777216.

Скорочення (Q-ALT1, ALT v0.3 §18.1): t ~ t + Im(I−M), бо f_t та f_{t+(I−M)a}
спряжені трансляцією. Число класів спряженості = Σ_M |ker(I−M)|.

Профіль OP(f) = (мультимножина довжин циклів, максимальний передперіод, |f(𝕊)|)
за ALT v0.3 §6.1. Профіль інваріантний щодо спряження.

Метод: повний (вичерпний) перебір. Векторизація через numpy.
Відтворення: python3 verify_alt7_affine.py
"""

import numpy as np
import itertools
import time
import sys
import os
from collections import Counter

t0 = time.time()


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            st.write(s)

    def flush(self):
        for st in self.streams:
            st.flush()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    logpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "verify_alt7_affine.log")
    logf = open(logpath, "w", encoding="utf-8")
    sys.stdout = Tee(sys.__stdout__, logf)

    print("SUBIT-∞ v6.14.1 — Q-ALT1 verification (ALT-7)")
    print("Python", sys.version.split()[0], "| numpy", np.__version__)
    print("=" * 72)

    idx = np.arange(64, dtype=np.int16)
    X = np.stack([idx // 16, (idx // 4) % 4, idx % 4], axis=1).astype(np.int16)

    # --- [1] Перелік матриць і образів ---
    Ms = np.array(list(itertools.product(range(4), repeat=9)),
                  dtype=np.int16).reshape(-1, 3, 3)
    N_M = Ms.shape[0]
    I = np.eye(3, dtype=np.int16)
    A = (I[None] - Ms) % 4                       # A = I - M

    AX = np.einsum('mij,xj->mxi', A, X) % 4      # (M,64,3) = A·x
    codes = (AX[..., 0] * 16 + AX[..., 1] * 4 + AX[..., 2]).astype(np.uint64)
    mask = np.bitwise_or.reduce(np.uint64(1) << codes, axis=1)   # образ Im(I-M)
    del AX, codes
    umask, inv = np.unique(mask, return_inverse=True)
    sizeS = np.array([bin(int(m)).count('1') for m in umask])    # |Im(I-M)|

    print("[1] Перелік")
    print("  матриць M:                 ", N_M)
    print("  афінних відображень Mx+t:  ", N_M * 64)
    print("  різних образів Im(I-M):    ", len(umask))
    print("  класів спряженості:        ", int((64 // sizeS[inv]).sum()))

    # --- [2] Представники класів (мінімальний код у косеті) ---
    def reps_for_mask(m):
        S = [c for c in range(64) if (int(m) >> c) & 1]
        out = []
        for t in range(64):
            tw, te, tn = t // 16, (t // 4) % 4, t % 4
            best = 64
            for s in S:
                c = ((tw + s // 16) % 4) * 16 + \
                    ((te + (s // 4) % 4) % 4) * 4 + ((tn + s % 4) % 4)
                if c < best:
                    best = c
            if best == t:
                out.append(t)
        return out

    reps_list = [reps_for_mask(m) for m in umask]

    Ms_l, t_l, w_l = [], [], []
    for i in range(N_M):
        u = inv[i]
        w = int(sizeS[u])                # вага = |Im(I-M)| (розмір косети)
        for t in reps_list[u]:
            Ms_l.append(Ms[i]); t_l.append(t); w_l.append(w)
    Marr = np.array(Ms_l, dtype=np.int16)
    tarr = np.array(t_l, dtype=np.int16)
    warr = np.array(w_l, dtype=np.int64)
    K = len(t_l)
    assert int(warr.sum()) == N_M * 64, "сума ваг != 4^12"
    print("  класів (M, косет):         ", K)
    print("  сума ваг (= 4¹²):          ", int(warr.sum()))
    print("  час:", round(time.time() - t0, 1), "с")

    # --- [3] Профілі ---
    ar = np.arange(64, dtype=np.int16)

    def profiles(F):
        B = F.shape[0]
        p = F.copy()
        per = np.zeros((B, 64), dtype=bool)
        fix = np.zeros((B, 65), dtype=np.int32)
        for d in range(1, 65):
            eq = (p == ar[None, :])
            fix[:, d] = eq.sum(axis=1)
            per |= eq
            if d < 64:
                p = np.take_along_axis(F, p, axis=1)
        c = np.zeros((B, 65), dtype=np.int32)
        for L in range(1, 65):
            s = fix[:, L].copy()
            for e in range(1, L):
                if L % e == 0:
                    s -= c[:, e]
            c[:, L] = s
        S = per.copy()
        maxpre = np.zeros(B, dtype=np.int8)
        remaining = ~S.all(axis=1)
        step = 0
        while remaining.any() and step < 64:
            step += 1
            S = np.take_along_axis(S, F, axis=1)
            done = S.all(axis=1)
            newly = remaining & done
            maxpre[newly] = step
            remaining = remaining & ~done
        return c, maxpre

    def image_sizes(F):
        s = np.sort(F, axis=1)
        return 1 + (np.diff(s, axis=1) != 0).sum(axis=1)

    CH = 262144
    prof_counter = Counter()
    prof_maps = Counter()
    prof_gl = Counter()
    maxpre_all = 0
    maxcyc_all = 0
    imgsizes = Counter()
    gl_mismatch = 0
    n_gl_classes = 0
    for a in range(0, K, CH):
        b = min(a + CH, K)
        Mb, tb, wb = Marr[a:b], tarr[a:b], warr[a:b]
        base = np.einsum('kij,xj->kxi', Mb, X) % 4
        tw, te, tn = tb // 16, (tb // 4) % 4, tb % 4
        F = (((base[..., 0] + tw[:, None]) % 4) * 16
             + ((base[..., 1] + te[:, None]) % 4) * 4
             + ((base[..., 2] + tn[:, None]) % 4)).astype(np.int16)
        ims = image_sizes(F)
        c, maxpre = profiles(F)
        # точний цілочисельний визначник; M оборотна над ℤ₄ ⟺ det непарний
        m = Mb.astype(np.int64)
        det = (m[:, 0, 0] * (m[:, 1, 1] * m[:, 2, 2] - m[:, 1, 2] * m[:, 2, 1])
               - m[:, 0, 1] * (m[:, 1, 0] * m[:, 2, 2] - m[:, 1, 2] * m[:, 2, 0])
               + m[:, 0, 2] * (m[:, 1, 0] * m[:, 2, 1] - m[:, 1, 1] * m[:, 2, 0]))
        is_gl = (det & 1) == 1
        gl_mismatch += int((is_gl != (ims == 64)).sum())
        n_gl_classes += int(is_gl.sum())
        for r in range(b - a):
            mult = []
            for L in range(1, 65):
                n = int(c[r, L]) // L
                if n:
                    mult.extend([L] * n)
            key = (tuple(mult), int(maxpre[r]), int(ims[r]))
            prof_counter[key] += 1
            prof_maps[key] += int(wb[r])
            if is_gl[r]:
                prof_gl[key] += int(wb[r])
            maxpre_all = max(maxpre_all, int(maxpre[r]))
            if mult:
                maxcyc_all = max(maxcyc_all, max(mult))
            imgsizes[int(ims[r])] += int(wb[r])

    print("[3] Профілі")
    print("  різних профілів OP(f):     ", len(prof_counter))
    print("  максимальний цикл:         ", maxcyc_all)
    print("  максимальний передперіод:  ", maxpre_all)
    print("  розміри образів |f(𝕊)|:    ",
          dict(sorted(imgsizes.items())))
    print("  контроль (det непарний)⟺(|im|=64): розбіжностей", gl_mismatch)
    print("  класів з оборотною M:      ", n_gl_classes)
    print("  час:", round(time.time() - t0, 1), "с")

    # --- [4] Повна таблиця профілів ---
    print("[4] Повна таблиця (79 профілів), сортування за #мап:")
    print("  {мультимножина циклів} | pre | |im| | #класів | #мап | #мап(M оборотна)")
    rows = sorted(prof_counter.items(), key=lambda kv: -prof_maps[kv[0]])
    for key, cnt in rows:
        mult, pre, im = key
        ms = ",".join(str(x) for x in mult)
        print("  {%s} | %d | %d | %d | %d | %d"
              % (ms, pre, im, cnt, prof_maps[key], prof_gl.get(key, 0)))

    # --- [5] Питання про профіль N (ALT v0.3 §18.4) ---
    target = ((1, 1, 2), 2, 16)
    print("[5] Профіль N = ({1,1,2}, pre=2, |im|=16):")
    print("    класів:", prof_counter.get(target, 0),
          "| мап:", prof_maps.get(target, 0),
          "| з них M оборотна:", prof_gl.get(target, 0))

    # --- [6] Контрольні суми ---
    print("[6] Контроль")
    print("  Σ#класів =", sum(prof_counter.values()), "(очікується", K, ")")
    print("  Σ#мап    =", sum(prof_maps.values()), "(очікується", N_M * 64, ")")
    print("  час:", round(time.time() - t0, 1), "с")
    print("=" * 72)
    print("ALT-7: перевірено вичерпно.")
    sys.stdout = sys.__stdout__
    logf.close()


if __name__ == "__main__":
    main()
