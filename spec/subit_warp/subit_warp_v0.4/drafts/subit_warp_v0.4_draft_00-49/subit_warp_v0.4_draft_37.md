# SUBIT-WARP v0.4 — W34.1.8 Stable Release Readiness Gate

**Статус:** RELEASE READINESS AUDIT · BLOCKED · NOT RELEASE CANDIDATE  
**Дата:** 5 листопада 2026 року  
**Робоча гілка:** `work/w34-1-3-corrected-integration`  
**Останній документний commit на момент аудиту:** `50120a485c3b228e632862c4f80d5ea38fcde803`  
**Базова система:** SUBIT-∞ v6.13.39 Stable  
**Принцип:** DO NOT COLLAPSE — CONTEXTUALIZE

## 1. Рішення

SUBIT-WARP v0.4 **не може бути позначений STABLE на поточному стані**. Цей аудит фіксує шлях до стабільного релізу й не створює псевдостатусу готовності.

Поточні документи W34.1.3–W34.1.7 усувають частину типових та інтеграційних неоднозначностей, але W23′ і W30 ще не оновлені, W20 full regression не виконаний, Lean kernel verification відсутня. Окремого доказу T-007P для часткового шару ще немає.

## 2. Поточна доказова база

| Об'єкт | Поточний стан |
|---|---|
| W23′ canonical source | Існує; не містить W34.1.5 інтеграції |
| W30 theorem registry | Існує; потребує окремих partial-layer записів |
| W34.1.3 total-code model | ANALYTICALLY CHECKED |
| W34.1.4 independent audit | CONDITIONAL PASS для математичного ядра; інтеграційні блокери описані |
| W34.1.5 Enc/Dec patch | TYPE-CORRECTED SPECIFICATION; NOT LEAN-VERIFIED |
| W34.1.6 review | CONDITIONAL PASS; R-01…R-06 |
| W34.1.7 W23′/W30 proposal | PROPOSAL ONLY; NOT APPLIED |
| W20 full regression | SPECIFIED; NOT EXECUTED |
| Lean 4 project/kernel | NOT VERIFIED |
| Rust implementation | NOT AUDITED |
| CI for latest documentation commit | No workflow runs/status checks returned; this is NOT a passing test result |

## 3. Release gates

### G-01 — Canonical W23′ integration

- Внести W34.1.7 §1–5 у нову редакцію W23′.
- Зберегти legacy `PartialTree_A^(b)` без ретроактивної fixed-point інтерпретації.
- Відокремити `PartialTree∞`, `Tω_P`, `Tω_P^+` від історичних типів.
- Уточнити локальні умови: `C_Partial^all` задавати TC-02/TC-03; TC-05 є permissive-правилом, а не повторним незалежним предикатом.
- Перевірити всі внутрішні посилання та типи метрик.

**Acceptance:** новий canonical blob SHA; відсутні неоднозначні або застарілі посилання; незалежний аудит diff PASS.

### G-02 — W30 theorem registry integration

- Додати T-001P та T-006P.
- Додати T-007P лише після повного доказу на partial-coded domain; до того статус PROOF REQUIRED.
- Не змінювати області T-001/T-006/T-007 без окремого обґрунтування.
- Перевірити залежності та реєстр статусів.

**Acceptance:** усі theorem IDs унікальні; кожне твердження має явні типи, припущення, залежності й рівень перевірки.

### G-03 — Independent canonical audit

Після G-01/G-02 виконати незалежний аудит:
- W23′ повністю;
- W30 повністю;
- усіх посилань W34.1.3–W34.1.7;
- усіх тверджень про Tω / Tω_P;
- усіх endpoint conventions;
- усіх статусів PROVED / CONDITIONAL / SPECIFIED.

**Acceptance:** жодного відкритого blocker, який впливає на коректність означень або заявлених теорем.

### G-04 — W20 full regression

Виконати нормативний набір, не підміняючи його вибірковими smoke tests:
- b ∈ {2,3,4,5};
- q ∈ {0,0.2,0.5,0.7,0.9,0.99}, із окремою обробкою q=1;
- n ∈ {0,1,2,3,4};
- c_q, λ_j, m_j, симетричність матриць, суми рядків, finite trace;
- спектральні кратності, апроксимації, q→1⁻;
- комутатор W15, оцінки Вейля;
- fingerprints та реконструкція;
- unary-вузли, root leaf, ABSENT/INTERNAL конфлікти;
- негативні тести для порушення TC-01…TC-05;
- контроль точності та відтворюваний лог.

**Acceptance:** повний звіт із середовищем, командами, параметрами, фактичними результатами, допусками й переліком усіх невдалих тестів. До запуску статус лишається NOT EXECUTED.

### G-05 — Lean formal verification

- Створити реальний Lean-проєкт, а не лише blueprint.
- Зафіксувати `lean-toolchain`, Lake manifest та версію Mathlib.
- Формалізувати базові алфавіти, адреси, total codes, PartialTree∞, Enc/Dec.
- Довести типову коректність, оберненість та ізометричність Enc/Dec.
- Формалізувати вибрані компактнісні та спектральні твердження з явними аксіомами.
- Запустити повний build і kernel check; зафіксувати команду, toolchain, commit і лог.
- Перевірити відсутність недозволених `sorry`, `admit` та непогоджених axioms.

**Acceptance:** відтворюваний успішний build і kernel-checked theorem inventory. Архітектурний blueprint не є проходженням цього gate.

### G-06 — Implementation audit

Rust gate застосовується, якщо Rust implementation входить до релізного обсягу. Якщо реліз є суто математичною специфікацією, Rust має бути явно позначений OUT OF SCOPE, а не «перевірений».

Для включеної реалізації потрібні:
- відповідність типів і даних канонічним означенням;
- property/regression tests;
- граничні та негативні випадки;
- детерміновані результати;
- звіт про відомі обмеження.

### G-07 — Documentation and release integrity

- Оновити README, індекс файлів, version map та статуси.
- Звірити всі SHA, шляхи й посилання.
- Прибрати суперечливі «current canonical» згадки.
- Підготувати release notes, changelog і відомі обмеження.
- Переконатися, що STABLE не поширюється на фізичні інтерпретації або відкриті дослідницькі гіпотези.
- Створювати release tag лише після проходження всіх обов'язкових gates.

## 4. Критерій STABLE

`SUBIT-WARP v0.4 STABLE` може бути затверджений лише за одночасного виконання:

`G-01 ∧ G-02 ∧ G-03 ∧ G-04 ∧ G-05 ∧ G-07`

G-06 є обов'язковим лише тоді, коли реалізація включена до заявленого релізного scope; в іншому разі необхідне явне виключення з scope.

Не допускається заміна фактичного проходження gate на:
- наявність специфікації тестів;
- аналітичний proof sketch;
- відсутність CI failure;
- відсутність workflow runs;
- успішний локальний тест лише частини параметрів;
- заяву про формалізацію без kernel-checked артефактів.

## 5. Наступна черга робіт

1. Незалежно перевірити W34.1.7 integration proposal.
2. Підготувати W23′ інтеграційну редакцію як окремий файл; не перезаписувати канон до review.
3. Підготувати W30 інтеграційну редакцію як окремий файл.
4. Провести diff review обох документів.
5. Лише потім оновити канонічні файли та почати W20/Lean execution.

## 6. Підсумковий вердикт

**SUBIT-WARP v0.4: BLOCKED — NOT STABLE — NOT RELEASE CANDIDATE.**

Математичне ядро має суттєву аналітичну основу, але стабільний реліз вимагає завершеної канонічної інтеграції, виконаного regression suite, формального підтвердження заявлених Lean-теорем і відтворюваної документації.

**DO NOT COLLAPSE — CONTEXTUALIZE.**
