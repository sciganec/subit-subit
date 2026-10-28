# Маніфест відтворюваності SUBIT-∞ v6.13.32

Git-репозиторію в проєкті немає, тому ідентифікатор збірки — SHA-256 файлів нижче. (Вимога аудиту «commit hash» закрита цим ідентифікатором: git-коміту для цього релізу немає і не створювалося.)

## Файли

| Файл | SHA-256 |
|---|---|
| SUBIT-inf_v6.13.32_stable.md | 21b2f70871d3076706fb8d6f0f133d171b7d10d7aeae06eec1f6122b55121eb0 |
| subit-lean-mathlib-v6.13.32.tar.gz (Lean: `pm/` без `.lake` і `*.olean`; 97 записів) | 9912e9a1f6f421c0005993653e59e5b59ff2cd93ffc51b5141e85d973ef52073 |
| subit-rust-v6.13.31.tar.gz (Rust-крейт без `target/`; без змін у v6.13.32) | bb371741adf71b3607c40931b5b49fc8171c0ce59e46ce8abab6b3815e6845d9 |
| REVIEW.md | 8a0cdba3279c6d00853128355dbfee603913909d89ba3c17335edba5c575ddc4 |
| lake-manifest.json | 701951fa03688a69962b010f7dd3b5dfd0730717cd8fc73fe5b1c9547a455af1 |
| lean-toolchain (`leanprover/lean4:v4.32.0`) | 2773c517aa90b66ea8a2c52bddddf84393157797f8341be0df45294fff7fd32e |
| rust_test_v6.13.31.log (`cargo test`: 57 passed) | d53f526868082f45e841e94943554405b5ad3fc11d3fa91ccd875ae38912dc10 |
| rust_clippy_v6.13.31.log (`cargo clippy --all-targets`: без попереджень) | 5a66711d7c4a4d3d460f0bf307b22058094203ac3d50f0a8c3390279e4851d70 |
| pilot01_v6.13.31.log (`cargo run --release --bin pilot01`: проходить) | 68df00dd568bd8942ed103e5ccb979dd68acb49e100f3b073eb4dc3e52ce428e |
| lean/build_v6.13.31.log (`lake build Subit` у робочому каталозі: 2467 задач) | ee50db48c682b51f8fb92dc0ddf9f4d75bab1bcd36cd5bd91ab0382c6ab83f51 |
| lean/build_repro_v6.13.32.log (відтворення збірки з архіву в окремому каталозі: 2467 задач, 0 попереджень) | 021ba9cb4c48407c10f9d0912a0f7e3f7a19e0f620c073bad878562e94834e90 |
| lean/axioms_v6.13.31.log (`#print axioms`) | d5c1110d75d083a7a534142af64043f7316ef7a45579a0774ee0cb9a567a78e3 |
| SUBIT-inf_v6.13.31_stable.md (попередня версія) | 536b51412d1179784021cd94de0750d10b64297cdda7920987f496b51be1fcda |

## Зміни відносно v6.13.31

- Текст (без змін тверджень і доказів): Pilot-01 перезапущено; §2.4′ доповнено звіркою з Lean і Rust (властивості на q < n збігаються; відмінність хвоста текст/Lean — 0 проти δ mod m — зафіксовано, обидва < m); BUILD-PASSED уточнено; Додатки Е і Ж синхронізовано з v6.13.32.
- Lean: змінено лише `REVIEW.md` (рядок v6.13.32). Код не змінювався.
- Rust: код і архів без змін (`subit-rust-v6.13.31.tar.gz`).

## Результати

- `lake build Subit`: 2467 задач, 0 попереджень (робочий каталог і відтворення з архіву).
- `#print axioms` для A4_general, W8G-теорем, extend_prod, extend_S_R, extend_ultra: лише propext, Classical.choice, Quot.sound.
- `grep sorry`: 4 файли, усі згадки в docstring-ах і коментарях.
- `cargo test`: 57 пройшли. `cargo clippy --all-targets`: без попереджень. Pilot-01: 2000 систем, 40755 точок, CHAOTIC 0, RESOURCE_EXCEEDED 0.
- Агентні перехресні перевірки: W8G — PASS WITH REMARKS (v6.13.28); ExtendProd і A4 — PASS WITH REMARKS, лише формулювання (v6.13.31).

## Відомі обмеження (відкриті)

- n > 64^63 для A4 — відкрито.
- Lemma 11.9 для компактних ультраметричних просторів поза Tree∞ і S∞ × ℛ₀ — не розглядалась. Тотожність d_ℛ(κ_c, κ_{c′}) = d_S(c, c′) у Lean не перевірена і для леми на добутку не потрібна.
- W8: нескінченність потребує StrictMono n; ATTAINED, NONMIN, h_top = 0 — лише hn: n_k ≥ k+1. Окремого об'єкта D∞ на S∞ × ℛ₀ не побудовано.
- Відтворення з нуля (з завантаженням Mathlib) не перевірялося; відтворення з архіву в окремому каталозі — проходить.
- Rust-тести перевіряють обрані розміри (a4_*_any_size: n ≤ 300 і окремі значення), а не всі n.
- Назва документа в Claude Docs досі «SUBIT-∞ v6.13.5» — перейменування вручну.
