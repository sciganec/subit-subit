# Маніфест відтворюваності SUBIT-∞ v6.13.34

Git-репозиторію в проєкті немає, тому ідентифікатор збірки — SHA-256 файлів нижче.

## Файли

| Файл | SHA-256 |
|---|---|
| SUBIT-inf_v6.13.34_stable.md | 36f6a353de5f2610dc9b982c69b2b3fbb9cd25f7a06c5e37b4df56ca86929751 |
| subit-lean-mathlib-v6.13.34.tar.gz (Lean: `pm/` без `.lake` і `*.olean`; 97 записів) | 2427b1f1c7a0cb0d563a8cf94df2a3b9edfa9b01957d9aa989d10141ddb3afaa |
| subit-rust-v6.13.31.tar.gz (Rust-крейт без `target/`; без змін з v6.13.31) | bb371741adf71b3607c40931b5b49fc8171c0ce59e46ce8abab6b3815e6845d9 |
| lean/pm/REVIEW.md | f6d18181f0ccf3a2bb1db0cdaae16868ffeacd04c5e20e6036198e6f5c98c3ad |
| lean/pm/lake-manifest.json | 701951fa03688a69962b010f7dd3b5dfd0730717cd8fc73fe5b1c9547a455af1 |
| lean/pm/lean-toolchain (`leanprover/lean4:v4.32.0`) | 2773c517aa90b66ea8a2c52bddddf84393157797f8341be0df45294fff7fd32e |
| rust_test_v6.13.31.log | d53f526868082f45e841e94943554405b5ad3fc11d3fa91ccd875ae38912dc10 |
| rust_clippy_v6.13.31.log | 5a66711d7c4a4d3d460f0bf307b22058094203ac3d50f0a8c3390279e4851d70 |
| pilot01_v6.13.31.log | 68df00dd568bd8942ed103e5ccb979dd68acb49e100f3b073eb4dc3e52ce428e |
| lean/build_v6.13.31.log | ee50db48c682b51f8fb92dc0ddf9f4d75bab1bcd36cd5bd91ab0382c6ab83f51 |
| lean/build_repro_v6.13.32.log | 021ba9cb4c48407c10f9d0912a0f7e3f7a19e0f620c073bad878562e94834e90 |
| lean/axioms_v6.13.31.log | d5c1110d75d083a7a534142af64043f7316ef7a45579a0774ee0cb9a567a78e3 |
| SUBIT-inf_v6.13.33_stable.md (попередня версія) | ef70fcd5fcdb9304506303f8a608004b7f6c893ab164ef487519c0d7dfdc6743 |

## Зміни відносно v6.13.33

- Текст: рішення щодо W6 і W7 — твердження залишено після перехресної перевірки агентом (PASS WITH REMARKS, без контрприкладів). Зауваження викладу внесено: W6 — скінченність пар β на відстані ≤ q; W7 — прибрано зайву фразу. Пояснення про MIN × NONATTAINED (§11.5) позначено як неповне; Q10′ — відкрите. Тверджень не додано.
- Lean: змінено лише `REVIEW.md`. Код не змінювався.
- Rust: без змін.

## Результати

- Lean: збірка з архіву в окремому каталозі — 2467 задач, 0 попереджень (`build_repro_v6.13.32.log`; код той самий).
- Аксіоми головних теорем: лише propext, Classical.choice, Quot.sound.
- cargo test: 57 пройшли; clippy: 0 попереджень; Pilot-01: CHAOTIC 0, RESOURCE_EXCEEDED 0.
- W6, W7: перехресна агентна перевірка — PASS WITH REMARKS. Lean-перевірки немає.

## Відомі обмеження

- Повне відтворення з нуля з Mathlib не перевірялося (CLEAN-REPRODUCIBLE-BUILD — ні; кеш Mathlib недоступний).
- W6, W7 — без Lean і без людського рецензування.
- Q10′ (MIN × NONATTAINED) — відкрито; пояснення в §11.5 — неповне міркування.
- A4 для n > 64^63 — відкрито. Lemma 11.9 поза Tree∞ і S∞ × ℛ₀ — не розглядалась.
- Назва проєкту в Claude Docs досі «SUBIT-∞ v6.13.5» — перейменування вручну.
