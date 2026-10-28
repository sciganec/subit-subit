# Маніфест відтворюваності SUBIT-∞ v6.13.35

Git-репозиторію в проєкті немає, тому ідентифікатор збірки — SHA-256 файлів нижче.

## Файли

| Файл | SHA-256 |
|---|---|
| SUBIT-inf_v6.13.35_stable.md | b2bd0abccc505371c39d0069e5d808c9c9b55e94baf0d5dbf34559f07cb1e9d0 |
| subit-lean-mathlib-v6.13.35.tar.gz (Lean: `pm/` без `.lake` і `*.olean`; 97 записів) | 55bf8e49f4f411d578cfaeda8c0bcf6313cc7c5c7a9b3bce55a3b29696387a63 |
| subit-rust-v6.13.31.tar.gz (Rust-крейт; без змін з v6.13.31) | bb371741adf71b3607c40931b5b49fc8171c0ce59e46ce8abab6b3815e6845d9 |
| lean/pm/REVIEW.md | 92b0eb2dcffd20afe370c41dd54dbb5c09b7a1f5308b9fdd6a611102d4d3d2e8 |
| lean/pm/lake-manifest.json | 701951fa03688a69962b010f7dd3b5dfd0730717cd8fc73fe5b1c9547a455af1 |
| lean/pm/lean-toolchain (`leanprover/lean4:v4.32.0`) | 2773c517aa90b66ea8a2c52bddddf84393157797f8341be0df45294fff7fd32e |
| lean/build_v6.13.35.log (`lake build Subit`, повна перебудова: 2467 задач, 0 попереджень) | b7f96a04d807f93a54c01314b6f59b969256b6222dffa7ae4b62832d3a174e65 |
| lean/checks/w8_chain_check_v6.13.35.lean (скрипт #print axioms для ланцюга W8) | fd1e91730b83f013d04c89fde2df7ac95b2487695ebdaafd9909b859dc239c38 |
| lean/checks/w8_chain_check_v6.13.35.log (результат: лише propext, Classical.choice, Quot.sound) | fb488b23ce3bdac44f0bcc200c05030c04069f51820fef926045b02b926631c7 |
| rust_test_v6.13.31.log | d53f526868082f45e841e94943554405b5ad3fc11d3fa91ccd875ae38912dc10 |
| rust_clippy_v6.13.31.log | 5a66711d7c4a4d3d460f0bf307b22058094203ac3d50f0a8c3390279e4851d70 |
| pilot01_v6.13.31.log | 68df00dd568bd8942ed103e5ccb979dd68acb49e100f3b073eb4dc3e52ce428e |
| lean/axioms_v6.13.31.log | d5c1110d75d083a7a534142af64043f7316ef7a45579a0774ee0cb9a567a78e3 |
| lean/build_repro_v6.13.32.log (збірка з архіву в окремому каталозі) | 021ba9cb4c48407c10f9d0912a0f7e3f7a19e0f620c073bad878562e94834e90 |
| SUBIT-inf_v6.13.34_stable.md (попередня версія) | 36f6a353de5f2610dc9b982c69b2b3fbb9cd25f7a06c5e37b4df56ca86929751 |

## Зміни відносно v6.13.34

- Текст: результат незалежної перевірки W8-ланцюга за кодом (PASS WITH REMARKS, контрприкладів немає). Уточнено: htop_omega_zero_G потребує лише hn; масштаб метрики dC/2 формально покрито htop_scale. BUILD-рядок доповнено повною перебудовою у v6.13.35. Тверджень не додано.
- Lean: змінено лише `REVIEW.md`. Код не змінювався.
- Rust: без змін.

## Результати

- `lake build Subit` у робочому каталозі, повна перебудова: 2467 задач, 0 попереджень (`lean/build_v6.13.35.log`). Попередні .olean частково були старші за джерела, тому це замінює попередні записи про збірку.
- Аксіоми ланцюга W8: лише propext, Classical.choice, Quot.sound.
- Збірка з архіву в окремому каталозі (v6.13.32): 2467 задач, 0 попереджень.

## Відомі обмеження

- Повне відтворення з нуля з Mathlib не перевірялося (CLEAN-REPRODUCIBLE-BUILD — ні).
- W6, W7 — без Lean; Q10′ відкрито.
- Перевірка W8-ланцюга — агентна, не людська.
- A4 для n > 64^63 відкрито; Lemma 11.9 поза Tree∞ і S∞ × ℛ₀ не розглядалась.
- Назва проєкту в Claude Docs досі «SUBIT-∞ v6.13.5» — перейменування вручну.
