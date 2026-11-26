# spec/ — специфікації SUBIT-∞

Хронологічний архів специфікацій. Усі версії зберігаються без вилучень.

---

## Поточний стабільний реліз

**[subit_infinity_spec_v6/subit_v6.13.37-39/](subit_infinity_spec_v6/subit_v6.13.37-39/)**

| Файл | Призначення |
| :-- | :-- |
| [`subit_v6.13.39_stable.md`](subit_infinity_spec_v6/subit_v6.13.37-39/subit_v6.13.39_stable.md) | Специфікація (заморожений текст) |
| [`subit_v6.13.37_lean_mathlib.tar.gz`](subit_infinity_spec_v6/subit_v6.13.37-39/subit_v6.13.37_lean_mathlib.tar.gz) | Lean 4.32.0 / Mathlib v4.32.0 (2472 задачі, 0 попереджень) |
| [`subit_v6.13.31_rust.tar.gz`](subit_infinity_spec_v6/subit_v6.13.37-39/subit_v6.13.31_rust.tar.gz) | Rust-крейт референтної реалізації (57 тестів) |
| [`w7_release_axioms_v6.13.37.lean`](subit_infinity_spec_v6/subit_v6.13.37-39/w7_release_axioms_v6.13.37.lean) | Скрипт перевірки аксіом W7 |
| [`subit_v6.13.39_manifest.md`](subit_infinity_spec_v6/subit_v6.13.37-39/subit_v6.13.39_manifest.md) | Хеші SHA-256 і відтворюваність |
| [`subit_v6.13.39_release_notes.md`](subit_infinity_spec_v6/subit_v6.13.37-39/subit_v6.13.39_release_notes.md) | Що змінено |
| [`subit_v6.13.39_review.md`](subit_infinity_spec_v6/subit_v6.13.37-39/subit_v6.13.39_review.md) | Журнал рецензування |

**Lean-перевірено:** W6 (W6Word, W6Tree), W7 (W7Abstract, W7Word, W7Tree), W8 (W8GTree), твердження Дод. Е.
Аксіоми: лише `propext`, `Classical.choice`, `Quot.sound`.

---

## Підготовка інтегрованого релізу v6.14 (Інтеграція ALT + WARP)

Серія інтегрованих специфікацій, що послідовно об'єднують стабільне ядро v6.13.39, алгебраїчно-модальну надбудову SUBIT-ALT та гранично-спектральну геометрію SUBIT-WARP.

| Редакція | Статус / Нововведення | Ключові артефакти |
| :-- | :-- | :-- |
| **[subit_v6.14.0/](subit_infinity_spec_v6/subit_v6.14.0/)** | Вихідна інтегрована чернетка (DRAFT · RC PREP) | [`subit_v6.14.0.md`](subit_infinity_spec_v6/subit_v6.14.0/subit_v6.14.0.md), 5-рівнева архітектура |
| **[subit_v6.14.1/](subit_infinity_spec_v6/subit_v6.14.1/)** | **ALT-7**: 79 орбітних профілів усіх $4^{12}$ афінних відображень (Q-ALT1 закрито); закриття E-REG-1..2, E-FLAG-1, E-ART-1; розділи TETRAKSIS та ECOSYSTEM | [`subit_v6.14.1.md`](subit_infinity_spec_v6/subit_v6.14.1/subit_v6.14.1.md), `verify_alt7_affine.py` |
| **[subit_v6.14.2/](subit_infinity_spec_v6/subit_v6.14.2/)** | **ALT-8**: структура $GL_3(\mathbb{Z}_4)$ (86016, розщеплення, 17 циклових типів, Q-ALT2 закрито); **ALT-9**: 36 класів бісимуляції $S5+N$ як добуток $3\times 4\times 3$ (Q-ALT3 закрито) | [`subit_v6.14.2.md`](subit_infinity_spec_v6/subit_v6.14.2/subit_v6.14.2.md), `verify_alt8_alt9.py` |
| **[subit_v6.14.3/](subit_infinity_spec_v6/subit_v6.14.3/)** | **ALT-10**: гібридна логіка на $\mathbb{F}$ (номінали $\leftrightarrow$ координатні атоми, Q-ALT4 закрито); **ALT-11**: динамічний контекст $M_k^b$ та комутація з $@$ (Q-ALT5 закрито) | [`subit_v6.14.3.md`](subit_infinity_spec_v6/subit_v6.14.3/subit_v6.14.3.md), `verify_alt10_alt11.py` |
| **[subit_v6.14.4/](subit_infinity_spec_v6/subit_v6.14.4/)** | **ALT-12**: епістемічна рамка 4 агентів, точні формули розподіленого $D$ та загального знання $C$ (Q-ALT7 закрито; RC CANDIDATE PREPARATION) | [`subit_v6.14.4.md`](subit_infinity_spec_v6/subit_v6.14.4/subit_v6.14.4.md), `verify_alt12.py` |

---

## Дослідницький модуль (SUBIT-WARP v0.4)

**[subit_warp/](subit_warp/)**

SUBIT-WARP v0.4 — формальна модель деревоподібних структур, граничної геометрії та ієрархічної спектральної динаміки (W0–W63). Статус: DRAFT · CANONICAL CONSOLIDATION · NOT STABLE.

Залежність: SUBIT-∞ v6.13.39 Stable (не змінює її означень).

| Файл | Зміст |
| :-- | :-- |
| [`subit_warp_v0.0_randall_sundrum.md`](subit_warp/subit_warp_v0.0/subit_warp_v0.0_randall_sundrum.md) | Вихідне есе: походження WARP-концепції |
| [`subit_warp_v0.1.md`](subit_warp/subit_warp_v0.1/subit_warp_v0.1.md) | Перша специфікація |
| [`subit_warp_v0.2.0.md`](subit_warp/subit_warp_v0.2/subit_warp_v0.2.0.md) | Редакція v0.2.0 |
| [`subit_warp_v0.3.md`](subit_warp/subit_warp_v0.3/subit_warp_v0.3.md) | Специфікація v0.3 Proof-Refined |
| [`subit_warp_v0.4.md`](subit_warp/subit_warp_v0.4/subit_warp_v0.4.md) | **Канонічна специфікація SUBIT-WARP v0.4 (Consolidated Canonical C2)** |
| [`subit_warp_v0.4_draft_13_canonical.md`](subit_warp/subit_warp_v0.4/drafts/subit_warp_v0.4_draft_00-49/subit_warp_v0.4_draft_13_canonical.md) | **W23′: Canonical Corrections after W24.16 (канонічна основа)** |
| `subit_warp/subit_warp_v0.4/drafts/` | Чернетки та аудити W0–W63 (дослідження граничної геометрії, спостережуваної еквівалентності та факторизацій) |

Деталі та повний список аудитів див. у [`subit_warp/README.md`](subit_warp/README.md).

---

## Альтернативні надбудови (SUBIT-ALT)

**[subit_alt/](subit_alt/)**

Альтернативні теоретичні надбудови над `subit_spec_v0.1.md` — не залежать від SUBIT-∞. Тор $\mathbb{Z}_4^3$, динаміка матриць, модальна логіка $S5^3$.

| Файл | Зміст |
| :-- | :-- |
| [`subit_alt_v0.1/01_intention.md`](subit_alt/subit_alt_v0.1/01_intention.md) | Аналіз природності розвитку v0.1 → v6; альтернативні шляхи |
| [`subit_alt_v0.1/02_intention_2.md`](subit_alt/subit_alt_v0.1/02_intention_2.md) | Продовження аналізу: індексикальність та тор $\mathbb{Z}_4^3$ |
| [`subit_alt_v0.1/subit_alt1_v0.1/subit_alt1_spec_v0.1.md`](subit_alt/subit_alt_v0.1/subit_alt1_v0.1/subit_alt1_spec_v0.1.md) | **SUBIT-ALT1**: $\mathbb{Z}_4^3$, 86016 оборотних матриць, ядерна гексаграма $N$ |
| [`subit_alt_v0.1/subit_alt2_v0.1-2/subit_alt2_spec_v0.1.md`](subit_alt/subit_alt_v0.1/subit_alt2_v0.1-2/subit_alt2_spec_v0.1.md) | **SUBIT-ALT2 v0.1**: контексти, $S5^3$, циклічний час, семантика Каплана |
| [`subit_alt_v0.1/subit_alt2_v0.1-2/subit_alt2_spec_v0.2.md`](subit_alt/subit_alt_v0.1/subit_alt2_v0.1-2/subit_alt2_spec_v0.2.md) | **ALT2 v0.2**: гексаграма як відношення доступності, бісимуляція |
| [`subit_alt_v0.3/subit_alt_v0.3_spec.md`](subit_alt/subit_alt_v0.3/subit_alt_v0.3_spec.md) | **SUBIT-ALT v0.3**: консолідована специфікація надбудови над 64 станами |

---

## Універсальна архітектура екосистеми

**[SUBIT_ECOSYSTEM/](SUBIT_ECOSYSTEM/)**

Універсальна мета-архітектура SUBIT-ECOSYSTEM: каталог 64 модулів, орієнтований граф залежностей $G_{SUBIT}$ (9 типів ребер), протокол обміну контекстними подіями та нормативний реєстр міжмодульних контрактів SCR.

| Специфікація | Зміст |
| :-- | :-- |
| [`01_SUBIT_ECOSYSTEM_UNIVERSAL_MASTER_SPECIFICATION_v0.1.0.md`](SUBIT_ECOSYSTEM/01_SUBIT_ECOSYSTEM_UNIVERSAL_MASTER_SPECIFICATION_v0.1.0.md) | Майстер-специфікація трьох масштабів (MICRO/MACRO/META) |
| [`02_SUBIT_64_MODULE_INTERDEPENDENCY_&_CROSS_MODULE_MATRIX_v1.0.md`](SUBIT_ECOSYSTEM/02_SUBIT_64_MODULE_INTERDEPENDENCY_&_CROSS_MODULE_MATRIX_v1.0.md) | Матриця міжмодульної взаємодії для 64 модулів |
| [`03_SUBIT_64_DEPENDENCY_GRAPH_&_CONTRACT_REGISTRY_v1.0.md`](SUBIT_ECOSYSTEM/03_SUBIT_64_DEPENDENCY_GRAPH_&_CONTRACT_REGISTRY_v1.0.md) | Граф залежностей та контрактний реєстр |
| [`04_SUBIT_64_CROSS_MODULE_CONTRACT_PROTOCOL_&_EVENT_EXCHANGE_SPECIFICATION_v1.0.md`](SUBIT_ECOSYSTEM/04_SUBIT_64_CROSS_MODULE_CONTRACT_PROTOCOL_&_EVENT_EXCHANGE_SPECIFICATION_v1.0.md) | Протокол обміну контекстними подіями |
| [`06_SUBIT_ECOSYSTEM_MASTER_TECHNICAL_SPECIFICATION_v0.1.0.md`](SUBIT_ECOSYSTEM/06_SUBIT_ECOSYSTEM_MASTER_TECHNICAL_SPECIFICATION_v0.1.0.md) | Master Technical Spec v0.1.0: реєстр SCR та політика сумісності |

---

## Генеративна морфологія (SUBIT-SHELL v1.0)

**[SUBIT_ECOSYSTEM/SUBIT_SHELL/](SUBIT_ECOSYSTEM/SUBIT_SHELL/)**

Комплексний генеративний теоретико-прикладний стек з 10 специфікацій: математична формалізація росту мушель (модель Раупа 1966), архітектура рушія, атлас 64 станів, механіка матеріалів та еволюційний аналіз простору форм.

| Документ | Тематика |
| :-- | :-- |
| [`01_SUBIT_SHELL_v1.0.md`](SUBIT_ECOSYSTEM/SUBIT_SHELL/01_SUBIT_SHELL_v1.0.md) | Загальна концепція та параметричний морфогенез |
| [`02_SUBIT_SHELL_MATHEMATICAL_FORMALIZATION_v1.0.md`](SUBIT_ECOSYSTEM/SUBIT_SHELL/02_SUBIT_SHELL_MATHEMATICAL_FORMALIZATION_v1.0.md) | Логарифмічні спіралі та диференціальна геометрія |
| [`03_SUBIT_SHELL_GENERATIVE_ENGINE_ARCHITECTURE_v1.0.md`](SUBIT_ECOSYSTEM/SUBIT_SHELL/03_SUBIT_SHELL_GENERATIVE_ENGINE_ARCHITECTURE_v1.0.md) | Архітектура генеративного обчислювального рушія |
| [`04_SUBIT_SHELL_MORPHOLOGICAL_CLASSIFICATION_&_64_STATE_ATLAS_v1.0.md`](SUBIT_ECOSYSTEM/SUBIT_SHELL/04_SUBIT_SHELL_MORPHOLOGICAL_CLASSIFICATION_&_64_STATE_ATLAS_v1.0.md) | Атлас 64 станів у морфопросторі Раупа ($W, D, T, S$) |
| [`05_SUBIT_SHELL_GROWTH_DYNAMICS_&_MORPHOGENESIS_THEORY_v1.0.md`](SUBIT_ECOSYSTEM/SUBIT_SHELL/05_SUBIT_SHELL_GROWTH_DYNAMICS_&_MORPHOGENESIS_THEORY_v1.0.md) – [`10_...`](SUBIT_ECOSYSTEM/SUBIT_SHELL/) | Динаміка росту, топологічна валідація, механіка матеріалів, калібрування природних видів та еволюційні патерни |

---

## Онтологічний каркас

**[subit_tetraksis/](subit_tetraksis/)**

Канонічна 4-рівнева, 10-вузлова онтологічна структура системи SUBIT (Monad → Dyad → Triad → Tetrad).

| Файл | Зміст |
| :-- | :-- |
| [`tetraksis_v0.2.md`](subit_tetraksis/tetraksis_v0.2.md) | Канонічна специфікація рівнів та вузлів TETRAKSIS |
| [`tetraksis_schema_v0.2.txt`](subit_tetraksis/tetraksis_schema_v0.2.txt) | Текстова схема та прогресія |

---

## Архів версій

| Папка / Файл | Версія | Дата |
| :-- | :-- | :-- |
| `subit_spec_v0.1.md` | v0.1 (прототип) | — |
| `subit_infinity_spec_v3.md` | v3 | Jul 2026 |
| `subit_infinity_spec_v4.md` | v4 | Jul 2026 |
| `subit_infinity_spec_v5.md` | v5 | Jul 2026 |
| `subit_infinity_spec_v5_2.md` | v5.2 | Aug 2026 |
| `subit_infinity_spec_v5_1_EXT/` | v5.1 EXT: монографія та коментарі | Oct 2026 |
| `subit_infinity_spec_v6/subit_v6.00/` | v6.00 | — |
| `subit_infinity_spec_v6/subit_v6.01-07/` | v6.01–6.07 | — |
| `subit_infinity_spec_v6/subit_v6.08/` | v6.08 | — |
| `subit_infinity_spec_v6/subit_v6.09/` | v6.09 | — |
| `subit_infinity_spec_v6/subit_v6.10/` | v6.10 | — |
| `subit_infinity_spec_v6/subit_v6.11/` | v6.11 | — |
| `subit_infinity_spec_v6/subit_v6.12/` | v6.12 | — |
| `subit_infinity_spec_v6/subit_v6.13.0-9/` | v6.13.0–9 | — |
| `subit_infinity_spec_v6/subit_v6.13.10-19/` | v6.13.10–19 | — |
| `subit_infinity_spec_v6/subit_v6.13.20-29/` | v6.13.20–29 | — |
| `subit_infinity_spec_v6/subit_v6.13.30-36/` | v6.13.30–36 | — |
| `subit_infinity_spec_v6/subit_v6.13.37-39/` | **v6.13.37–39 (STABLE)** | Nov 2026 |
| `subit_infinity_spec_v6/subit_v6.14.0/` | v6.14.0 (Draft / Initial Integration) | Nov 2026 |
| `subit_infinity_spec_v6/subit_v6.14.1/` | v6.14.1 (Draft / ALT-7 Affine Profiles) | Nov 2026 |
| `subit_infinity_spec_v6/subit_v6.14.2/` | v6.14.2 (Draft / ALT-8 GL3(Z4), ALT-9 Bisimulation) | Nov 2026 |
| `subit_infinity_spec_v6/subit_v6.14.3/` | v6.14.3 (Draft / ALT-10 Hybrid, ALT-11 Monster Commutation) | Nov 2026 |
| `subit_infinity_spec_v6/subit_v6.14.4/` | **v6.14.4 (RC CANDIDATE / ALT-12 Epistemic Frame)** | Nov 2026 |

Принцип: **незворотність**. Жодна версія не вилучається.
