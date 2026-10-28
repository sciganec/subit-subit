# Маніфест відтворюваності SUBIT-∞ v6.13.33

Git-репозиторію в проєкті немає, тому ідентифікатор збірки — SHA-256 файлів нижче. Вимога «commit hash» (аудит v6.13.30) закрита цим ідентифікатором; git-коміту не створювалося.

## Файли

| Файл | SHA-256 |
|---|---|
| SUBIT-inf_v6.13.33_stable.md | ef70fcd5fcdb9304506303f8a608004b7f6c893ab164ef487519c0d7dfdc6743 |
| subit-lean-mathlib-v6.13.33.tar.gz (Lean: `pm/` без `.lake` і `*.olean`; 97 записів) | 1011d84d3650a63fb7aa88c57db9c189c169d49714164a4d9d79ae55606d74b5 |
| subit-rust-v6.13.31.tar.gz (Rust-крейт без `target/`; без змін у v6.13.32–v6.13.33) | bb371741adf71b3607c40931b5b49fc8171c0ce59e46ce8abab6b3815e6845d9 |
| lean/pm/REVIEW.md | 966b3576bd64342f321aefc4d674063061066f2527bd1bf8b6c0669ff944f95c |
| lean/pm/lake-manifest.json | 701951fa03688a69962b010f7dd3b5dfd0730717cd8fc73fe5b1c9547a455af1 |
| lean/pm/lean-toolchain (`leanprover/lean4:v4.32.0`) | 2773c517aa90b66ea8a2c52bddddf84393157797f8341be0df45294fff7fd32e |
| rust_test_v6.13.31.log (`cargo test`: 57 passed) | d53f526868082f45e841e94943554405b5ad3fc11d3fa91ccd875ae38912dc10 |
| rust_clippy_v6.13.31.log (`cargo clippy --all-targets`: без попереджень) | 5a66711d7c4a4d3d460f0bf307b22058094203ac3d50f0a8c3390279e4851d70 |
| pilot01_v6.13.31.log (`cargo run --release --bin pilot01`, перезапуск у v6.13.32) | 68df00dd568bd8942ed103e5ccb979dd68acb49e100f3b073eb4dc3e52ce428e |
| lean/build_v6.13.31.log (`lake build Subit` у робочому каталозі: 2467 задач) | ee50db48c682b51f8fb92dc0ddf9f4d75bab1bcd36cd5bd91ab0382c6ab83f51 |
| lean/build_repro_v6.13.32.log (збірка з архіву в окремому каталозі: 2467 задач, 0 попереджень) | 021ba9cb4c48407c10f9d0912a0f7e3f7a19e0f620c073bad878562e94834e90 |
| lean/axioms_v6.13.31.log (`#print axioms`) | d5c1110d75d083a7a534142af64043f7316ef7a45579a0774ee0cb9a567a78e3 |
| SUBIT-inf_v6.13.32_stable.md (попередня версія) | 21b2f70871d3076706fb8d6f0f133d171b7d10d7aeae06eec1f6122b55121eb0 |

## Зміни відносно v6.13.32

- Текст (без змін тверджень і доказів): виправлено DOC-01…DOC-06 з аудиту v6.13.32: історія Pilot-01 узгоджена (перезапуск у v6.13.32; історичний — з v6.13.19); BUILD-PASSED розділено на BUILD-PASSED-FROM-ARCHIVE (частково) і CLEAN-REPRODUCIBLE-BUILD (ні); визначення «стабільна» прямо не означає конформності; назву Rust-архіву і хеш виправлено; додано таблицю точних гіпотез і висновків W8G-теорем (за сигнатурами Lean).
- Lean: змінено лише `REVIEW.md` (рядок v6.13.33). Код не змінювався.
- Rust: код і архів без змін.

## Результати

- Збірка Lean з архіву в окремому каталозі: 2467 задач, 0 попереджень (лог `build_repro_v6.13.32.log`, код без змін відносно v6.13.32).
- `#print axioms` (v6.13.31, код той самий): лише propext, Classical.choice, Quot.sound.
- `cargo test`: 57 пройшли. `cargo clippy --all-targets`: без попереджень. Pilot-01: 2000 систем, 40755 точок, CHAOTIC 0, RESOURCE_EXCEEDED 0.

## Відомі обмеження (відкриті)

- Повне відтворення з нуля, з завантаженням Mathlib, не перевірялося (статус CLEAN-REPRODUCIBLE-BUILD — ні).
- Звірка гіпотез W8G-теорем і конкретного ланцюга W8GCount → W8GEntropy виконана за сигнатурами, а не як окрема незалежна перевірка коду; агентна перевірка W8G — PASS WITH REMARKS (v6.13.28).
- n > 64^63 для A4 — відкрито. Lemma 11.9 поза Tree∞ і S∞ × ℛ₀ — не розглядалась.
- Rust-тести перевіряють обрані розміри, а не всі n. Статус IMPLEMENTED (conformant) — ні; EMPIRICALLY SUPPORTED — ні.
- Назва проєкту в Claude Docs досі «SUBIT-∞ v6.13.5» — перейменування вручну.
