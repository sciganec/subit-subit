# Маніфест відтворюваності SUBIT-∞ v6.13.37

Git-репозиторію в проєкті немає, тому ідентифікатор збірки — SHA-256 файлів нижче.

## Файли

| Файл | SHA-256 |
|---|---|
| SUBIT-inf_v6.13.37_stable.md | 8587555d4a621d894e971360c8dd5b62627335141c6c472dec8056596f74019d |
| subit-lean-mathlib-v6.13.37.tar.gz (Lean: `pm/` без `.lake` і `*.olean`; 104 записи, включно з каталогами; містить `pm/checks/`) | 3f4d5e0df4df2bff84503ce1ec012af6384761695475c976f75ea5e065daf728 |
| subit-rust-v6.13.31.tar.gz (Rust-крейт; без змін з v6.13.31) | bb371741adf71b3607c40931b5b49fc8171c0ce59e46ce8abab6b3815e6845d9 |
| lean/pm/REVIEW.md | 770ed1c8c07bfdd7a31c5683ed3b4cd7f2e35c2c5799e084e7e47248000ef1d5 |
| lean/pm/lake-manifest.json | 701951fa03688a69962b010f7dd3b5dfd0730717cd8fc73fe5b1c9547a455af1 |
| lean/pm/lean-toolchain (`leanprover/lean4:v4.32.0`) | 2773c517aa90b66ea8a2c52bddddf84393157797f8341be0df45294fff7fd32e |
| lean/pm/Subit.lean (реєстр; додано `Subit.W7Abstract`, `Subit.W7Word`, `Subit.W7Tree`) | 89745eb87367fefc40c54859d29cc0eee9939707103fb33459329a6533ddb709 |
| lean/pm/Subit/W7Abstract.lean (нове) | 1b164da184908e31a849121eeb4fb66f6c67ef6167892b04cc151bb9fa97a1e1 |
| lean/pm/Subit/W7Word.lean (нове) | b0fb7ccd46ef47a84b043f85456fad12cb2acf7815dd42edff7b532291bd27c5 |
| lean/pm/Subit/W7Tree.lean (нове) | 22a8a46be7a46fa2e7efaa3b6a7ba3c6452533f8ff4c4c5e9c125252ceb7296f |
| lean/pm/Subit/W6Tree.lean (змінено: прибрано глобальний `set_option`, попередження усунено через `omit`) | 130d57b2caf73caab7d4cce9e6e9710ebfff4d6473623a6439e8e4cd984f11ad |
| lean/pm/Subit/Sanity.lean | 177589dd390eeb5ac7f3b0d3ce42dc5eb355c5f97185f30ae6c55b92b3e38e71 |
| lean/pm/Subit/Sanity139.lean | 9d352e864ec044a0325ef3722eb27d30c982d936f7066d94e532f97e0a14bccf |
| lean/pm/checks/w7_release_axioms_v6.13.37.lean (скрипт #print axioms, 13 теорем; тепер у архіві) | a4a4aedf13afb17a9cb8e1ad1e3f4b2b4f92aed2959a57ed969ce2ab0f49d432 |
| lean/build_v6.13.37.log (`lake build` у робочому дереві, інкрементальна: 2472 задачі, 0 попереджень) | 6673ac3542ed240b79d24817ece8be2ec506d82c52035e1b378551e0eb561361 |
| lean/sanity_build_v6.13.37.log (`lake build Subit.Sanity Subit.Sanity139`: 0 попереджень) | 608c4bf1a89d87c232dd6db5c647ea63523c1a3eddf540394b8e73bb68f5b3a6 |
| lean/clean_build_v6.13.37.log (`lake build` з розпакованого архіву в окремому каталозі: 2472 задачі, 0 попереджень; 63 модулі Subit скомпільовано з нуля) | 60aadcf9e31cf9e1743e197bf853b6dd2a101e8349aa7da451c7379bef03147e |
| lean/clean_sanity_v6.13.37.log (Sanity у тому ж чистому дереві: 0 попереджень) | aa78b6e733d74f6c764010d29c635d1a9ad9187ebbafdfa61fd392e3d87cbd2a |
| lean/checks/w7_release_axioms_v6.13.37.lean (копія скрипта аксіом поза архівом) | a4a4aedf13afb17a9cb8e1ad1e3f4b2b4f92aed2959a57ed969ce2ab0f49d432 |
| lean/checks/w7_release_axioms_v6.13.37.log (лише propext, Classical.choice, Quot.sound) | b10a2f9f982671212d84059b7501cc78fba5c2314a49fe00fa4ea49919db77ad |
| lean/checks/w7_release_axioms_clean_v6.13.37.log (повторний запуск у чистому дереві; побайтово той самий вивід) | b10a2f9f982671212d84059b7501cc78fba5c2314a49fe00fa4ea49919db77ad |

Попередні записи з v6.13.36 (W6, логи W8, Rust, Pilot-01) — без змін; див. `MANIFEST-v6.13.36.md`.

## Зміни відносно v6.13.36

- Lean: нові модулі `Subit/W7Abstract.lean`, `Subit/W7Word.lean`, `Subit/W7Tree.lean`; реєстр `Subit.lean`. Код W8 не змінено; W6 — лише прибрано глобальний `set_option` (тверджень і доказів не змінено).
- Перейменовано `W7Word.dW7_hypotheses_discharged` → `dW7_applicability` (перевірка застосовності гіпотез; не математичне твердження).
- Sanity-модулі: виправлено 3 попередження (`_`-префікси); збираються окремо.
- Текст: статус W7 змінено з DP-f на LEAN-CHECKED (§11.6, таблиця статусів, реєстр); тверджень не змінено; уточнено формулювання W7 (підслово в u_N; порядок слів у Lean); рядок журналу v6.13.37.
- Rust: без змін.

## Результати

- Інкрементальна `lake build` у робочому дереві: 2472 задачі, 0 попереджень.
- Чиста збірка з архіву: розпаковано в окремий каталог без `.olean`, залежності Mathlib підключено з готових пакетів; 63 модулі Subit скомпільовано з нуля; 0 попереджень, 0 помилок. Mathlib не перекомпільовано.
- Sanity-модулі: 0 попереджень в обох збірках.
- Аксіоми 13 ключових теорем W7: лише propext, Classical.choice, Quot.sound; у робочому і чистому дереві вивід побайтово однаковий.
- Заборонені слова (`sorry`, `admit`, `native_decide`, `axiom`) у трьох W7-файлах не знайдено; `set_option` у W7-файлах немає.
- `set_option linter.unnecessarySeqFocus false in` у `Subit/Tree.lean` (рядок 27) лишився навмисно: точковий, з обґрунтуванням у коментарі, поза W7.
- Перехресна перевірка (агент), чотири проходи: (1) FAIL лише з бухгалтерії, математика підтверджена; (2) PASS WITH REMARKS, зауваження внесено; (3) контрольний прохід на фінальному стані: PASS WITH REMARKS, блокуючих немає. Зауваження щодо скрипта аксіом поза архівом і застарілої копії архіву закрито в цьому релізі. Четвертий (цей) — після остаточних змін у W6Tree і архіві — не проводився; зміни в Lean-коді порівняно з контрольним проходом відсутні, змінено лише W6Tree (перевірено збіркою і чистою збіркою) та REVIEW/MANIFEST.

## Відомі обмеження

- Повне відтворення з нуля включно з Mathlib не перевірялося (CLEAN-REPRODUCIBLE-BUILD — лише рівень Subit).
- Перевірка W7 — агентна, не людська; людського рецензента немає за домовленістю.
- Q10′ (MIN × NONATTAINED для MIN_ZERO і MIN_POS) — відкрито; W6 і W7 покривають NONMIN × NONATTAINED для своїх класів.
- A4 для n > 64^63 відкрито; Lemma 11.9 поза Tree∞ і S∞ × ℛ₀ не розглядалась.
- Назва проєкту в Claude Docs досі «SUBIT-∞ v6.13.5» — перейменування вручну.
- Рядок W7 у таблиці статусів рецензентського документа в Claude Docs не додано (API не приймає вставку рядка таблиці); додати вручну.
