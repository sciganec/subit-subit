# Маніфест відтворюваності SUBIT-∞ v6.13.28

Git-репозиторію в проєкті немає, тому ідентифікатор збірки — SHA-256 файлів нижче.

## Файли

| Файл | SHA-256 |
|---|---|
| SUBIT-inf_v6.13.28_stable.md | e351ea85f067541b96316ab1482e4bee20bb49dc9737080d03c4cb426a66664c |
| subit-lean-mathlib-v6.13.28.tar.gz (архів Lean: W8G-модулі, реєстрація в `Subit.lean`) | 747ccef1ab9002c066d139d9350ba684f01397d500211dfa0caf76fa5370312c |
| REVIEW.md | 9d696ae67e7fc086af068b1b48655fcd34652a0b6a5afafdda2516f91d12410b |
| lake-manifest.json | 701951fa03688a69962b010f7dd3b5dfd0730717cd8fc73fe5b1c9547a455af1 |
| lean-toolchain | 2773c517aa90b66ea8a2c52bddddf84393157797f8341be0df45294fff7fd32e |
| SUBIT-inf_v6.13.27_stable.md (попередня версія, замінена v6.13.28) | c2844956f2ab748b78635c696ff4e0482825f364677a8a3d51db863e41d3c80b |
| subit-lean-mathlib-v6.13.25.tar.gz (попередній архів Lean) | 1d09c6b83360ab0347572e7118f8aa944aab7ef536ec5abbb4f78d4c35d3689d |

Чернетку маніфесту `MANIFEST_v6.13.25_stale_draft.md` (хеш d6d1…) не публікувати.

## Середовище Lean

- lean-toolchain: `leanprover/lean4:v4.32.0`
- Збірка: `lake build Subit` у каталозі `pm`: 2466 jobs, успішно.
- Mathlib зібрано з вихідного коду (кеш недоступний через проксі).

## Залежності (lake-manifest.json, без змін)

mathlib `81a5d257c8e410db227a6665ed08f64fea08e997`; plausible `e12c1910fe855cbfc38803cd4e55543906d5fa62`; LeanSearchClient `c5d5b8fe6e5158def25cd28eb94e4141ad97c843`; importGraph `7e9612bf0b9ee66db3cb5b9988a35afc706f5a12`; proofwidgets `6e311e2a844da9b2cc3971187df2fe0066947b93`; aesop `a7dbf0c63b694e47f425f3dcddbc0e178bb432d3`; Qq `38d591e778f100aec9762bb582f9c7f55f50e9dc`; batteries `023ce7d62a0531e22a5331e20b587817a80d49ff`; Cli `88679d088c9720c27ebdf2ba4dafe17341747f94`.

## Результати

- `grep sorry` у `Subit/W8G*.lean`: порожньо.
- `#print axioms` (стандартні аксіоми: propext, Classical.choice, Quot.sound): `Subit.W8GAttained.w8G_summary`, `Subit.W8GEntropy.htop_omega_zero_G`, `Subit.W8G.factor_bound_G`, `Subit.W8GTree.w8G_tree_summary`, `Subit.W8GTree.htop_TY_zero`, `Subit.W8GAttained.omega_infinite_G`, `Subit.W8GAttained.nonmin_G`. `Subit.W8G.dG_eq` — `propext`, `Quot.sound`.
- Незалежний аудит W8G-порту: PASS WITH REMARKS, блокуючих зауважень немає. Виправлено docstring-и `W8GAttained` і `W8GTree`. Записано: невикористаний `hn` в `image_omegaG`, стиль `push_neg`.
- Rust (`rust/subit-rust.tar.gz`, sha256 6f8124d5…): не змінювався в цьому релізі; 57 тестів, clippy чистий (перевірено у v6.13.25).

## Відомі обмеження

- W8: для довільних strictly зростаючих n_k (`hn : ∀ k, k+1 ≤ n k`; `hmono : StrictMono n` лише для нескінченності) — LEAN-CHECKED на Tree∞ і графі G.
- Lemma 11.9: вкладеність класів і база f_0 — відкрито (remark аудиту v6.13.25).
- A4 (§2.4′): 1 ≤ n ≤ 64^63.
