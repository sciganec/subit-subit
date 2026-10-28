# Маніфест відтворюваності SUBIT-∞ v6.13.27 (супроводжує v6.13.25 без змін коду)

Git-репозиторію в проєкті немає, тому ідентифікатор збірки — SHA-256 файлів нижче.

## Файли

| Файл | SHA-256 |
|---|---|
| SUBIT-inf_v6.13.27_stable.md | c2844956f2ab748b78635c696ff4e0482825f364677a8a3d51db863e41d3c80b |
| SUBIT-inf_v6.13.26_stable.md (замінено v6.13.27: уточнення без зміни тверджень) | 38787616409db30037d6c3e49fb289b92fabcc1d59202c47b4b6b3c906a2c87b |
| SUBIT-inf_v6.13.25_stable.md (замінено v6.13.26 через блокуючий залишок §12) | c2f1df7726ee60f3b22aab326ad7a4f89a92caa9e2170dec4026922c0c29850f |
| SUBIT-inf_v6.13.24_stable.md | f83d7a6c4e0ec863b46e3fa77750b326ad1e422006238a36e1fca62a65f244a7 |
| subit-lean-mathlib-v6.13.25.tar.gz (архів Lean; код Lean не змінено відносно v6.13.24, змінено лише REVIEW.md) | 1d09c6b83360ab0347572e7118f8aa944aab7ef536ec5abbb4f78d4c35d3689d |
| REVIEW.md | 14c6533e1a248c0457e579e5f606055209e6d26f71b7a6d4b9dce0760ec9bd1a |
| lake-manifest.json | 701951fa03688a69962b010f7dd3b5dfd0730717cd8fc73fe5b1c9547a455af1 |

## Середовище Lean

- lean-toolchain: `leanprover/lean4:v4.32.0`
- Команда збірки: `lake build` (повна, 2461 jobs), у каталозі `pm`.
- Кеш Mathlib (`lake exe cache get`) недоступний через проксі (403); Mathlib зібрано з вихідного коду.

## Залежності (lake-manifest.json)

| Пакет | Версія/rev | Джерело |
|---|---|---|
| mathlib | `81a5d257c8e410db227a6665ed08f64fea08e997` | https://github.com/leanprover-community/mathlib4 |
| plausible | `e12c1910fe855cbfc38803cd4e55543906d5fa62` | https://github.com/leanprover-community/plausible |
| LeanSearchClient | `c5d5b8fe6e5158def25cd28eb94e4141ad97c843` | https://github.com/leanprover-community/LeanSearchClient |
| importGraph | `7e9612bf0b9ee66db3cb5b9988a35afc706f5a12` | https://github.com/leanprover-community/import-graph |
| proofwidgets | `6e311e2a844da9b2cc3971187df2fe0066947b93` | https://github.com/leanprover-community/ProofWidgets4 |
| aesop | `a7dbf0c63b694e47f425f3dcddbc0e178bb432d3` | https://github.com/leanprover-community/aesop |
| Qq | `38d591e778f100aec9762bb582f9c7f55f50e9dc` | https://github.com/leanprover-community/quote4 |
| batteries | `023ce7d62a0531e22a5331e20b587817a80d49ff` | https://github.com/leanprover-community/batteries |
| Cli | `88679d088c9720c27ebdf2ba4dafe17341747f94` | https://github.com/leanprover/lean4-cli |

## Результати

- Збірка: успішна, без `sorry` у модулях W8 та A4 (grep); попередження лінтера — косметичні.
- `#print axioms` (v6.13.24 Lean-код): `Subit.W8Tree.w8_tree_summary`, `Subit.W8Tree.nonmin_graph`, `Subit.W8Tree.minOn_TY_of_graph` — `propext`, `Classical.choice`, `Quot.sound`.
- Незалежний аудит W8Spine/W8Tree: PASS WITH REMARKS (зауваження виправлено у v6.13.24 або записано).
- Порівняно з архівом v6.13.24: відрізняється лише REVIEW.md (журнал і заголовок).
- Rust-тести (57) у цій збірці не перезапускалися; цифри — з v6.13.19.

## Відомі обмеження

- W8: n_k = k+1 (довільні strictly зростаючі n_k не формалізовано).
- A4 (§2.4′): 1 ≤ n ≤ 64^63.
