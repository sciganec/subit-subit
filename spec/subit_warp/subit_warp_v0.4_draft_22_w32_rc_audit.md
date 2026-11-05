# SUBIT-WARP v0.4
## W32 — Canonical v0.4 Integration & Release Candidate Audit

**Версія:** v0.4-W32  
**Статус:** INTEGRATION & RELEASE CANDIDATE AUDIT · NOT STABLE  
**Дата:** 4 листопада 2026 року  
**Тип:** інтеграційний аудит перед редакційними виправленнями релізу  
**Об'єкт:** увесь каталог `spec/subit_warp/` (локально: `C:\Users\sciga\subit-subit\spec\subit_warp\`)  
**Базова система:** SUBIT-∞ v6.13.39 Stable (поза межами цього аудиту; не змінюється)  
**Інтегровані матеріали:** W0–W31, README WARP, попередні аудити репозиторію (4 листопада 2026)  
**Принцип:** DO NOT COLLAPSE — CONTEXTUALIZE  

---

# W32.0. Призначення

W32 є **інтеграційним аудитом Release Candidate** перед будь-якими масовими правками репозиторію.

Він **не** оголошує STABLE, **не** переписує канон і **не** застосовує виправлення. Його завдання:

1. зафіксувати інвентар усіх файлів WARP і розбіжність між «заявленим каноном» і фактичним станом дерева;
2. звести статуси тверджень / етапів W0–W31 в одну таблицю;
3. перелічити блокери для Release Candidate і для STABLE;
4. задати обов'язкові кроки інтеграції (посилання, README, поглинання виправлень W29, виконавчі артефакти W25/W20);
5. винести вердикт: **NOT READY FOR STABLE** з умовами RC;
6. зберегти принцип **DO NOT COLLAPSE — CONTEXTUALIZE**: аналітичне, чисельне, формальне і реалізаційне не зливаються в один ярлик.

W32 виконує роль, яку вже анонсовано в кінці W31:

> інтегрувати W23–W31 у єдину канонічну редакцію, усунути розбіжності між документами, перевірити повноту доказів і сформувати остаточний перелік блокерів перед присвоєнням статусу STABLE.

Цей документ є саме тим аудитом; наступна канонічна редакція (умовно W23″ / W33) має з'явитися **після** виконання інтеграційних кроків нижче.

---

# W32.1. Інвентар файлів WARP

## W32.1.1. Повний список (локально, 4 листопада 2026)

| Файл | Роль / вміст | Примітка |
| :-- | :-- | :-- |
| `README.md` | Опис модуля, таблиця файлів, статус | **Застарілий:** зупиняється на W24.16 / W23′; наступним етапом називає W25; биті посилання на `draft_12_audit_3` |
| `subit_warp_00_randall_sundrum.md` | Вихідне есе Randall–Sundrum | Історичний |
| `subit_warp_v0.1.md` | Специфікація v0.1 | Історичний |
| `subit_warp_v0.2.0.md` | Специфікація v0.2.0 | Історичний |
| `subit_warp_v0.2.1.md` | Редакція v0.2.1 | Історичний |
| `subit_warp_v0.2_audit.md` | Аудит v0.2 | Історичний |
| `subit_warp_v0.3.md` | Первинна Proof-Refined специфікація (W0–…) | **Первинне джерело** для W24.16 |
| `subit_warp_v0.3_audit_1.md` … `_5.md` | Аудити v0.3 (W6–W9 тощо) | Історичні |
| `subit_warp_v0.4.0.md` | **W21** Canonical Specification | Консолідація v0.4.0 |
| `subit_warp_v0.4_draft_1.md` … `_9.md` | Чернетки еволюції v0.4 | Історичні |
| `subit_warp_v0.4_draft_10_audit.md` | **W22** Audit-Refined | Блокери F01–F12; передумова W23 |
| `subit_warp_v0.4_draft_11_canonical.md` | **W23** Canonical Corrections | Історичний канон (до W24.16) |
| `subit_warp_v0.4_draft_12_audit_2.md` | **W24** Primary Source Audit | Частковий; addendum → W24.16 |
| `subit_warp_v0.4_draft_13_canonical.md` | **W23′** Canonical після W24.16 | **Заявлений** поточний канон у README |
| `subit_warp_v0.4_draft_14_audit_3.md` | **W24.16** Primary Source Audit W0–W6 | Фактичний файл; раніше згадувався як `draft_12_audit_3` |
| `subit_warp_v0.4_draft_15_audit_4.md` | **W25** Executable Verification | COMPLETED (аналітика + чисельно) |
| `subit_warp_v0.4_draft_16_audit_5.md` | **W26** Canonical Integration & Release Audit | INTEGRATION CANDIDATE · NOT STABLE |
| `subit_warp_v0.4_draft_17.md` | **W27** Proof Closure | ANALYTICAL PROOF CLOSURE — COMPLETED |
| `subit_warp_v0.4_draft_18.md` | **W28** Global Consistency & Regression Spec | SPEC COMPLETED; W20 NOT EXECUTED |
| `subit_warp_v0.4_draft_19.md` | **W29** Independent Mathematical Audit | **CORRECTIONS REQUIRED** (C-11…C-15) |
| `subit_warp_v0.4_draft_20.md` | **W30** Theorem Registry & Proof Dependency | MATHEMATICALLY CONSOLIDATED DRAFT |
| `subit_warp_v0.4_draft_21.md` | **W31** Formalization Boundary & Lean Blueprint | Lean architecture SPECIFIED; impl NOT STARTED |
| `subit_warp_v0.4_draft_22_w32_rc_audit.md` | **W32** (цей документ) | RC integration audit |

**Відсутній файл:** `subit_warp_v0.4_draft_12_audit_3.md` — на нього все ще посилаються README, `draft_12_audit_2` (addendum) і `draft_13_canonical`, але локально його замінено / перейменовано на `draft_14_audit_3`.

## W32.1.2. Заявлений канон vs фактичний стан

| Питання | Заявлено (README / draft_13) | Фактично в дереві |
| :-- | :-- | :-- |
| Поточна канонічна редакція | `draft_13_canonical` = W23′ | Файл існує; але **не поглинув** виправлення W25–W29 (границя q→1 у нормах, q⁰=1, ordered/unordered fingerprint, C-11…C-15) |
| Останній завершений етап | README: «наступний етап — W25» | W25–W31 уже написані локально |
| Файл W24.16 | `draft_12_audit_3.md` | Реально: `draft_14_audit_3.md`; `draft_12_audit_3` **немає** |
| Статус модуля | DRAFT · NOT STABLE | Підтверджено всіма W25–W31 |
| Єдиний реєстр теорем | Не в README | Є в W30 (T-001…); **не інтегрований** у `draft_13` |
| Lean-межа | Відкрито (W10) | W31 задає blueprint; реалізації немає |
| Математична зрілість після W30/W31 | Не відображено | «MATHEMATICALLY CONSOLIDATED DRAFT», Stable **не** approved |

**Висновок інвентарю:** README і `draft_13` описують стан **після W24.16 / W23′**. Локальне дерево вже містить **вісім** пізніших документів (W24.16-копія + W25–W31). Канон **заявлений**, але **не інтегрований**. Це головна структурна проблема Release Candidate.

---

# W32.2. Зведена карта статусів W0–W31

Легенда статусів (узгоджена з W24.16 / W29 / W30):

- **PASS** — етап / блок закритий у своїй ролі.
- **PASS WITH CONDITIONS** — коректний за явних умов / обмежень області.
- **CORRECTIONS REQUIRED** — потрібні зміни формулювань перед інтеграцією в канон.
- **OPEN** — не виконано або поза межами поточного RC.
- **SUPERSEDED** — замінений пізнішою редакцією (зберігається як історія).

## W32.2.1. Етапи еволюції

| ID | Файл | Статус етапу | Коментар |
| :-- | :-- | :-- | :-- |
| W0–W6 (v0.3) | `subit_warp_v0.3.md` | PASS WITH CONDITIONS | Первинне джерело; W5 потребував Tω⁺ (закрито в W23′ / W27) |
| W7–W10 | v0.3 + аудити | PASS WITH CONDITIONS | Спектр / параметри; Lean і повна чисельна сертифікація матриць — OPEN |
| W11–W20 | v0.3 / drafts | PASS WITH CONDITIONS / OPEN | Математика частково; **W20 suite NOT EXECUTED** |
| W21 | `v0.4.0.md` | SUPERSEDED (як канон) | Історична консолідація |
| W22 | `draft_10_audit` | PASS (як аудит) | Визначив блокери; багато закриті пізніше |
| W23 | `draft_11_canonical` | SUPERSEDED | Замінений W23′ після W24.16 |
| W24 | `draft_12_audit_2` | PASS WITH CONDITIONS | Частковий; доповнений W24.16 |
| W24.16 | `draft_14_audit_3` | PASS (COMPLETED WITH CORRECTIONS) | Первинний аудит W0–W6 завершено |
| W23′ | `draft_13_canonical` | PASS WITH CONDITIONS | Поточний **заявлений** канон; **не** містить C-11…C-15 і висновків W25 |
| W25 | `draft_15_audit_4` | PASS | ANALYTICALLY + NUMERICALLY VERIFIED; Lean/Rust NOT EXECUTED |
| W26 | `draft_16_audit_5` | PASS WITH CONDITIONS | INTEGRATION CANDIDATE; STABILITY NOT ACHIEVED |
| W27 | `draft_17` | PASS | Proof closure трьох питань W26 |
| W28 | `draft_18` | PASS WITH CONDITIONS | Regression **specification** completed; execution OPEN |
| W29 | `draft_19` | **CORRECTIONS REQUIRED** | Незалежний аудит: C-11…C-15 обов'язкові |
| W30 | `draft_20` | PASS WITH CONDITIONS | Реєстр теорем; Stable NOT YET APPROVED |
| W31 | `draft_21` | PASS (як blueprint) | Lean architecture SPECIFIED; implementation OPEN |
| W32 | `draft_22` (цей файл) | COMPLETED AS AUDIT | RC audit; без правок репо |

## W32.2.2. Ключові математичні блоки (зріз W30 + W29)

| Блок | Аналітика | Чисельно (W25) | Lean | Реалізація |
| :-- | :-- | :-- | :-- | :-- |
| Типи дерев Full / Partial / Finite | PASS (W23′ / W30) | н/п | OPEN | OPEN |
| Метрики d_F, d_Σ, d_T, d_H | PASS (W23′ / W24.16) | н/п | OPEN | OPEN |
| Grafting / контрактність | PASS | н/п | OPEN | OPEN |
| Boundary Lipschitz на Tω⁺ | PASS (W27 / W29-02) | н/п | OPEN | OPEN |
| Hausdorff dim повної межі | PASS WITH CONDITIONS (посилення викладу) | н/п | OPEN | OPEN |
| Спадне ядро / спектр T_q | PASS | PASS (W25) | OPEN | OPEN |
| Зростаюче ядро / K_Vl(ξ,ξ)=0 | PASS (W23′ / W29) | н/п | OPEN | OPEN |
| q=0 / q=1 endpoints | PASS WITH CONDITIONS | PASS (аналітика W25) | OPEN | OPEN |
| Trace finite vs infinite | PASS (W29 C-13) | PASS (скінченні) | OPEN | OPEN |
| Параметрична ліпшицевість T_q | PASS (W27 / W29-03) | н/п | OPEN | OPEN |
| Fingerprint unordered | PASS WITH CONDITIONS | н/п | OPEN | OPEN |
| Fingerprint ordered | CORRECTIONS REQUIRED → розділити (W29 C-12) | н/п | OPEN | OPEN |
| Конвенція q⁰=1 | CORRECTIONS REQUIRED (W29 C-11) | н/п | OPEN | OPEN |
| W20 regression suite | SPECIFIED (W28) | OPEN (не виконано) | OPEN | OPEN |
| Lean formalization | Blueprint (W31) | н/п | OPEN | OPEN |
| Rust / executable audit | н/п | Частково W25 (матриці) | н/п | OPEN |

## W32.2.3. Обов'язкові виправлення W29, ще не в каноні

Ці пункти **не** поглинуті `draft_13_canonical` і блокують «чистий» RC-канон:

1. **C-11. Zero-power convention** — `q⁰ = 1` для `q ∈ [0,1]`.
2. **C-12. Ordered fingerprint separation** — неупорядкована і впорядкована реконструкції — різні теореми.
3. **C-13. Trace separation** — `Tr(T_q^(n))` ≠ `Tr(T_q)`.
4. **C-14. Endpoint separation** — формули для `0 ≤ q < 1` і `q = 1` окремо.
5. **C-15. Kernel threshold separation** — пороги обмеженості та HS для зростаючого ядра не об'єднуються.

Додатково з W25 (ще не в каноні):

6. **Операторна vs слідова збіжність при q→1⁻:** `T_q → T₁` в операторній нормі, але **не** в слідовій (`lim ‖T_q‖₁ = 2`, тоді як `‖P_const‖₁ = 1`).

---

# W32.3. Блокери Release Candidate

Розділяємо два рівні (принцип CONTEXTUALIZE):

## W32.3.1. Блокери для оголошення **Release Candidate** (математичний RC-документ)

Без закриття цих пунктів не можна чесно сказати «канон v0.4 RC»:

| # | Блокер | Де | Вага |
| :- | :-- | :-- | :-- |
| B1 | Биті посилання на `draft_12_audit_3` (файл відсутній; є `draft_14_audit_3`) | README, draft_12_audit_2 addendum, draft_13 | Критичний для узгодженості репо |
| B2 | README WARP не знає про draft_14–21 / W25–W31; «наступний етап W25» застарів | README.md | Критичний |
| B3 | Заявлений канон W23′ не поглинув C-11…C-15 і застереження W25 про норми при q→1 | draft_13 vs W29/W25 | Критичний для математичного RC |
| B4 | Немає **єдиного** канонічного документа після W29 (реєстр у W30, докази в W27, виправлення в W29 — розкидані) | draft_13 / 17 / 19 / 20 | Критичний |
| B5 | Імена файлів не відповідають номерам етапів (draft_14 = W24.16, draft_15 = W25, …) | увесь каталог | Середній (плутає аудит і посилання) |
| B6 | Кореневий README репозиторію описує WARP як W21–W24 / draft_11 і «дерево v0.3» | `README.md` репо (поза WARP; фіксуємо як зовнішній блокер узгодженості) | Середній |

## W32.3.2. Блокери для оголошення **STABLE** (повний реліз)

Навіть після інтеграції канону STABLE **заборонений**, доки не виконано (узгоджено з W28 release gate / W30 G-01…G-13):

| # | Блокер | Статус зараз |
| :- | :-- | :-- |
| S1 | Повне виконання W20 regression suite + reproducibility report | NOT EXECUTED |
| S2 | Lean: хоча б задекларований scope + старт P0 (W31); зараз implementation NOT STARTED | OPEN |
| S3 | Окремий audit реалізації (Rust / інший executable шар) vs математичне ядро | NOT AUDITED |
| S4 | Єдиний канонічний документ + єдиний реєстр теорем + єдиний реєстр відкритих проблем | IN PROGRESS (є шматки) |
| S5 | Усі обов'язкові розділення типів/метрик/endpoints/fingerprint/trace внесені в канон | Частково (W23′ так; W29 ні) |
| S6 | Жодне NUMERICALLY VERIFIED не видається за FORMALLY VERIFIED | Дотримується в текстах; треба зберегти в RC |

**W32 не вимагає S1–S3 для самого факту існування RC-чернетки**, але вимагає **явно винести** їх за межі математичного RC з аргументованим рішенням (як дозволяє W28.13).

---

# W32.4. Обов'язкові кроки інтеграції (після W32; ще не виконані)

Порядок рекомендований; W32 їх **не виконує**.

## Крок I-1. Виправити посилання на W24.16

- Або повернути ім'я `subit_warp_v0.4_draft_12_audit_3.md`,  
- або оновити всі посилання на `subit_warp_v0.4_draft_14_audit_3.md` у:
  - `spec/subit_warp/README.md`,
  - `subit_warp_v0.4_draft_12_audit_2.md` (addendum),
  - `subit_warp_v0.4_draft_13_canonical.md`.

## Крок I-2. Синхронізувати README WARP

- Версія / еволюція: W21–W31 (і W32 як RC-audit).
- Таблиця файлів: додати draft_14–22.
- «Поточна канонічна редакція»: залишати `draft_13` **лише до** появи наступного канону; після поглинання W29 — новий файл (наприклад W23″ / draft_23_canonical).
- «Наступний етап»: не W25 (уже є), а **інтеграція канону + виконання W20 / старт Lean P0** за рішенням власника.

## Крок I-3. Поглинути виправлення W29 (і застереження W25) у наступний канон

Новий канонічний документ повинен явно містити:

- C-11…C-15;
- правило операторної ≠ слідової збіжності при q→1⁻;
- збережені вже в W23′: d_F / d_Σ / d_T / d_H, PartialTree як розширення, Tω⁺, W5.4′, K_Vl(ξ,ξ)=0;
- посилання на реєстр W30 (T-001…) без дублювання суперечливих формул.

**Не згортати** історію: W23 і W23′ залишаються як попередні редакції (CONTEXTUALIZE).

## Крок I-4. Виконавчий шар W25 / W28

- Зберегти W25 як звіт незалежної перевірки (вже є).
- Реалізувати або явно відкласти **W20 full suite** з окремим статусом EXECUTED vs SPECIFIED.
- Не змішувати 84 конфігурації W25 зі статусом «уся система перевірена».

## Крок I-5. Зовнішня узгодженість репозиторію (поза редагуванням infinity-spec)

- Оновити кореневий README щодо WARP (W23′, W25–W32), **не** чіпаючи тексти SUBIT-∞ v6.13.39 у цьому проході.
- Окремим комітом (коли буде дозвіл) — артефакти поза WARP з попереднього аудиту репо (SHA256SUMS, Kircher, Rust-архів, `.gitignore` / `*.log`).

## Крок I-6. Після інтеграції — короткий W33 / RC checklist

Повторно прогнати лише:

- наявність усіх файлів з таблиці README;
- відсутність битих відносних посилань у `spec/subit_warp/`;
- наявність секції «що входить у Mathematical RC» vs «що відкладено до STABLE».

---

# W32.5. Критерії Mathematical Release Candidate

W32 пропонує **розділити** ярлики:

### A. `MATHEMATICAL RC` (дозволений після I-1…I-3)

Умови:

1. Єдиний канонічний md з поглинутими W24.16 + W25-застереженням + W29 C-11…C-15.
2. README WARP синхронний з деревом файлів і статусами.
3. Немає битих посилань на W24.16.
4. Реєстр теорем W30 узгоджений з каноном (або канон явно делегує до W30).
5. Явно написано: Lean / W20 / Rust — **поза** Mathematical RC.
6. Статус документа: `CANONICAL MATHEMATICAL RC · NOT SOFTWARE-STABLE · NOT LEAN-VERIFIED`.

### B. `STABLE` (не дозволений зараз)

Потрібні додатково S1–S5 з §W32.3.2.

### C. Заборонені ярлики на поточному зрізі

- `STABLE`
- `LEAN VERIFIED`
- `IMPLEMENTATION VERIFIED`
- `W20 PASSED` (без звіту виконання)

---

# W32.6. Вердикт W32

## Коротко

**SUBIT-WARP v0.4 — NOT READY FOR STABLE.**

**Release Candidate (математичний) — NOT YET DECLARED:** математичне ядро після W27–W30 виглядає **консолідованим під умовами**, але канонічний файл і README **відстають** від W25–W31, а W29 лишає обов'язкові правки (C-11…C-15) поза `draft_13`.

## Розгорнуто

1. **Сильні сторони:** первинний аудит W0–W6 (W24.16) завершено; W23′ фіксує d_F/d_Σ/Tω⁺/PartialTree/K_Vl; W25 підтверджує спектральні формули чисельно в обмеженому діапазоні; W27 закриває три аналітичні дірки; W30 дає реєстр без циклів залежностей; W31 окреслює Lean без претензії на верифікацію.
2. **Слабкі сторони для RC:** биті refs на W24.16; README «застряг» на W25-as-next; канон не поглинув W29; немає одного інтегрованого RC-документа.
3. **Слабкі сторони для STABLE:** W20 не виконано; Lean не розпочато; Rust/executable audit окремо не зроблено.
4. **Дозволений наступний крок:** виконати інтеграційні кроки I-1…I-3, потім оголосити **Mathematical RC**; S1–S3 тримати відкритими з явним scope.
5. **Цей документ (W32)** є аудитом і картою блокерів; він **не** є новим каноном і **не** змінює SUBIT-∞.

## Фінальні мітки

```
SUBIT-WARP v0.4 STATUS .............. DRAFT · NOT STABLE
MATHEMATICAL CORE ................... CONSOLIDATED WITH CONDITIONS (W27–W30)
CANONICAL FILE ...................... draft_13 (W23′) — STALE vs W25–W29
W29 CORRECTIONS ..................... NOT ABSORBED INTO CANON
W25 EXECUTABLE ...................... PARTIAL (spectral matrices); W20 NOT EXECUTED
LEAN ................................ BLUEPRINT ONLY (W31)
RUST / IMPLEMENTATION AUDIT ......... NOT DONE
RELEASE CANDIDATE ................... NOT DECLARED (blocked by I-1…I-3)
STABLE .............................. NOT APPROVED
```

---

# W32.7. Принцип

Кожен рівень лишається окремим:

**Structure ≠ Geometry ≠ Measure ≠ Interaction ≠ Spectrum ≠ Reconstruction**  
**Analytically verified ≠ Numerically verified ≠ Formally verified ≠ Implementation audited**  
**Canonical draft ≠ Release Candidate ≠ Stable**

Інтеграція означає **узгодити контексти**, а не злити їх в один статус.

**DO NOT COLLAPSE — CONTEXTUALIZE.**

---

# W32.8. Наступний етап (поза цим файлом)

Після затвердження власником:

1. Застосувати I-1…I-3 (WARP-only правки).
2. За потреби — окремий коміт зовнішніх артефактів репо (не infinity-spec).
3. Створити наступний канон (умовно **W23″ / W33 Canonical RC**).
4. Лише тоді розглядати ярлик `MATHEMATICAL RC`.

Кінець W32.
