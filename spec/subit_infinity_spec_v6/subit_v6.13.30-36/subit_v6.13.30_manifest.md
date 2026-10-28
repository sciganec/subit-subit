# Маніфест відтворюваності SUBIT-∞ v6.13.30

Git-репозиторію в проєкті немає, тому ідентифікатор збірки — SHA-256 файлів нижче.

## Файли

| Файл | SHA-256 |
|---|---|
| SUBIT-inf_v6.13.30_stable.md | 9d6c75a23f5d2c72bc7e1302fead0b8bcc6ab762716d704cc28e91dceec8f4c4 |
| subit-lean-mathlib-v6.13.30.tar.gz (архів Lean: нові ExtendProd.lean, Subit.lean, REVIEW.md) | cdcbea7a0f0c58f45c66d72437d0c13968e3825ba63c390081a7df269f4305dc |
| REVIEW.md | 1132ffe4a1a1750c03bba4535baeb51fa71127b17aea953036460e02b4595e51 |
| lake-manifest.json | 701951fa03688a69962b010f7dd3b5dfd0730717cd8fc73fe5b1c9547a455af1 |
| lean-toolchain | 2773c517aa90b66ea8a2c52bddddf84393157797f8341be0df45294fff7fd32e |
| SUBIT-inf_v6.13.29_stable.md (попередня версія) | d185b71973eb19350a9d05186dd1fbfa8588313b5e72d3ada4e2e9e980c13968 |

## Зміни відносно v6.13.29

- Текст: лише статус леми 11.9 для S∞ × ℛ₀ (DP-f → LEAN-CHECKED); твердження без змін.
- Lean: новий модуль `Subit/ExtendProd.lean` (`instIsUltrametricDistProd`, `extend_prod`, `extend_S_R`); усі 33 попередження лінтера прибрано.

## Результати

- `lake build Subit` (повна перебудова всіх модулів): успішно, 0 попереджень.
- `#print axioms` (стандартні propext, Classical.choice, Quot.sound): `extend_S_R`, `extend_prod`, `instIsUltrametricDistProd`, `W8GTree.w8G_tree_summary`, `W8GAttained.w8G_summary`, `W8Tree.w8_tree_summary`, `W8G.factor_bound_G`.
- `sorry`: лише в коментарях і docstring-ах (перевірено grep).

## Відомі обмеження

- Lemma 11.9 для компактних ультраметричних просторів поза S∞ × ℛ₀ / Tree∞ — не розглядалась окремо.
- W8: для довільних strictly зростаючих n_k (hn: n_k ≥ k+1; hmono: StrictMono n лише для нескінченності) — LEAN-CHECKED.
- A4 (§2.4′): 1 ≤ n ≤ 64^63.
