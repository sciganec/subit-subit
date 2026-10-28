# Маніфест відтворюваності SUBIT-∞ v6.13.29

Git-репозиторію в проєкті немає, тому ідентифікатор збірки — SHA-256 файлів нижче.

## Файли

| Файл | SHA-256 |
|---|---|
| SUBIT-inf_v6.13.29_stable.md | d185b71973eb19350a9d05186dd1fbfa8588313b5e72d3ada4e2e9e980c13968 |
| subit-lean-mathlib-v6.13.29.tar.gz (архів Lean: код без змін, REVIEW.md оновлено) | 26738319d525422495c0c2a953109627201c48b2382d85be6ade1bbee3cdc928 |
| REVIEW.md | 3c32bb8302eeb6093e959d12aa3acaaf2a53600931751bb0773a75ed44393558 |
| lake-manifest.json | 701951fa03688a69962b010f7dd3b5dfd0730717cd8fc73fe5b1c9547a455af1 |
| lean-toolchain | 2773c517aa90b66ea8a2c52bddddf84393157797f8341be0df45294fff7fd32e |
| SUBIT-inf_v6.13.28_stable.md (попередня версія) | e351ea85f067541b96316ab1482e4bee20bb49dc9737080d03c4cb426a66664c |

## Зміни відносно v6.13.28

- Текст: доведення леми 11.9 (твердження без змін). Перевірено агентом, PASS WITH REMARKS.
- Lean-код без змін; архів v6.13.29 відрізняється від v6.13.28 лише REVIEW.md.

## Результати (з v6.13.28)

- `lake build Subit`: успішно (2466 jobs); `grep sorry` у W8G-файлах порожній; аксіоми стандартні.

## Відомі обмеження

- W8: для довільних strictly зростаючих n_k (hn: n_k ≥ k+1; hmono: StrictMono n лише для нескінченності) — LEAN-CHECKED на Tree∞ і графі G.
- Лема 11.9 для S∞ × ℛ₀ — DP-f (Lean: лише Tree∞).
- A4 (§2.4′): 1 ≤ n ≤ 64^63.
