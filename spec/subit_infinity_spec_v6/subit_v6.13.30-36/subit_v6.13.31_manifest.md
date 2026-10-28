# Маніфест відтворюваності SUBIT-∞ v6.13.31

Git-репозиторію в проєкті немає, тому ідентифікатор збірки — SHA-256 файлів нижче.

## Файли

| Файл | SHA-256 |
|---|---|
| SUBIT-inf_v6.13.31_stable.md | 536b51412d1179784021cd94de0750d10b64297cdda7920987f496b51be1fcda |
| subit-lean-mathlib-v6.13.31.tar.gz (архів Lean: `pm/` без `.lake` і `*.olean`; 97 записів) | 24241e62746102a4f2fbd7e8db4e678e3cb8f317bb6e21b6589eef42c4e926f3 |
| subit-rust-v6.13.31.tar.gz (крейт `subit` без `target/`; 28 записів) | bb371741adf71b3607c40931b5b49fc8171c0ce59e46ce8abab6b3815e6845d9 |
| REVIEW.md | f8ee91cc37f3f0b6e80296110d6511f6075d8b199de1aafa2ee70576c3734758 |
| lake-manifest.json | 701951fa03688a69962b010f7dd3b5dfd0730717cd8fc73fe5b1c9547a455af1 |
| lean-toolchain (`leanprover/lean4:v4.32.0`) | 2773c517aa90b66ea8a2c52bddddf84393157797f8341be0df45294fff7fd32e |
| rust_test_v6.13.31.log (`cargo test`: 57 passed) | d53f526868082f45e841e94943554405b5ad3fc11d3fa91ccd875ae38912dc10 |
| rust_clippy_v6.13.31.log (`cargo clippy --all-targets`: без попереджень) | 5a66711d7c4a4d3d460f0bf307b22058094203ac3d50f0a8c3390279e4851d70 |
| build_v6.13.31.log (`lake build Subit`: 2467 задач) | ee50db48c682b51f8fb92dc0ddf9f4d75bab1bcd36cd5bd91ab0382c6ab83f51 |
| axioms_v6.13.31.log (`#print axioms`) | d5c1110d75d083a7a534142af64043f7316ef7a45579a0774ee0cb9a567a78e3 |
| SUBIT-inf_v6.13.30_stable.md (попередня версія) | 9d6c75a23f5d2c72bc7e1302fead0b8bcc6ab762716d704cc28e91dceec8f4c4 |
| subit-rust.tar.gz (попередній Rust-архів, до v6.13.31) | 6f8124d54bb1685cd87b4b703b37a024e4e03bde94ae3c1838919926ba071ed9 |

## Зміни відносно v6.13.30

- Текст (без змін тверджень і доказів): §0.1 уточнено (BUILD-PASSED — часткове; RUST-TESTED — перезапуск; LEAN-CHECKED — W8 для довільних strictly зростаючих n_k, ExtendProd, A4 з 1 ≤ n ≤ 64^63); Додаток Е: заголовок синхронізовано, кількість задач 2467, таблиця «Загальний випадок W8» з точними іменами теорем, W8 у переліку «Не формалізовано» з уточненням; Додаток Ж: cargo test і clippy перезапущено; застарілі формулювання A4 (рядок про закриття Q22, Додаток Б, журнал v6.12) позначено як частково закрите / застаріле.
- Lean: змінено лише docstring у `Subit/A4.lean`. Математичний код не змінено.
- Rust: змінено лише docstring у `src/plus.rs` (межа 1 ≤ n ≤ 64^63). Код не змінено.
- REVIEW.md: заголовок до v6.13.31; рядок v6.13.31 додано; застарілу позначку про відсутність агентної перевірки ExtendProd виправлено.

## Результати

- `lake build Subit` (повна перебудова модулів): успішно, 2467 задач, попереджень немає.
- `#print axioms` (перевірено заново для v6.13.31): `A4_general`, `W8G.factor_bound_G`, `W8GEntropy.htop_omega_zero_G`, `W8GAttained.attained_G`, `W8GAttained.nonmin_G`, `W8GAttained.omega_infinite_G`, `W8GTree.w8G_tree_summary`, `extend_prod`, `extend_S_R`, `extend_ultra`: лише propext, Classical.choice, Quot.sound.
- `grep sorry`: 4 файли, усі згадки лише в docstring-ах і коментарях; доказових термів з sorry в архіві не знайдено (це grep-перевірка, не формальна).
- `cargo test`: 57 пройшли. `cargo clippy --all-targets`: без попереджень.
- Агентні перехресні перевірки: W8G — PASS WITH REMARKS (v6.13.28); ExtendProd і A4 — PASS WITH REMARKS, лише формулювання (v6.13.31).

## Відомі обмеження (відкриті, не закриті цим релізом)

- Звірка текстової формули A4 з Lean поріг-за-порогом (зокрема хвіст останнього неповного блоку) не проведена; Lean доводить існування правил rule, g з властивостями, а не конкретну формулу з §2.4′.
- A4: 1 ≤ n ≤ 64^63; n > 64^63 — відкрито.
- Lemma 11.9 для компактних ультраметричних просторів поза Tree∞ і S∞ × ℛ₀ — не розглядалась. Тотожність d_ℛ(κ_c, κ_{c′}) = d_S(c, c′) у Lean не перевірена і для леми 11.9 на добутку не потрібна.
- W8: нескінченність потребує StrictMono n; ATTAINED, NONMIN, h_top = 0 — лише hn: n_k ≥ k+1. Окремого об'єкта D∞ на S∞ × ℛ₀ не побудовано.
- Pilot-01 у v6.13.31 не перезапускалося (останній запуск — з v6.13.19).
- Відтворюваність на чистому середовищі (окремо від цієї сесії) не перевірялася; BUILD-PASSED — часткове.
- Назва документа в Claude Docs ще містить «v6.13.5» — перейменування вручну (агентська сторона цього не дозволяє).
