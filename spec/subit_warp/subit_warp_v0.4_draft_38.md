# SUBIT-WARP v0.4 — W34.1.9 Independent Review of W34.1.7 Integration Proposal

**Статус:** CONDITIONAL PASS · PROPOSAL REVIEW · CANONICAL INTEGRATION NOT AUTHORIZED YET  
**Дата:** 5 листопада 2026 року  
**Об'єкт:** `subit_warp_v0.4_draft_36.md` (W34.1.7)  
**Перевірена редакція:** blob `4e3e9f70b2ca311dd8c96054c796cc309c3a1b62`  
**Джерела:** W23′ `draft_13_canonical.md`; W30 `draft_20.md`; W34.1.3–W34.1.6  
**Принцип:** DO NOT COLLAPSE — CONTEXTUALIZE

## 1. Вердикт

W34.1.7 коректно обирає консервативну стратегію інтеграції: не переписує legacy `PartialTree_A^(b)`, не підміняє історичний `Tω` новим `Tω_P`, не переписує T-006/T-007 без окремого доказу. Це правильне рішення для збереження семантичної сумісності W23′/W30.

Після редакційного уточнення метрик і часткової межі пропозиція є придатною для підготовки інтеграційних файлів. Проте **безпосередньо перезаписувати W23′/W30 за цим документом ще не слід**: потрібен повний line-by-line diff, перевірка всіх внутрішніх посилань і завершення T-007P.

## 2. Перевірки, що пройшли

- Legacy partial type зберігається без ретроактивного μ/ν-рішення.
- `PartialTree∞` отримує явну greatest-fixed-point семантику.
- `C_Partial^all` визначається через TC-02/TC-03; TC-05 не дублюється як незалежний предикат.
- Rooted class `C_Partial` є clopen restriction за кореневою координатою.
- `Enc_sub/Dec_sub` працюють на all-класі; rooted Enc/Dec є обмеженнями.
- Історичні `Tω/Tω⁺` не ототожнюються з `Tω_P/Tω_P⁺`.
- Метрики `d_P`, `d_Full`, `d_code` відокремлені; адресна `d_Σ` не змішується з ними.
- Часткова межа `∂_P p` отримала явне покоординатне означення.
- T-007P не оголошено доведеним без повного перенесення аргументу.

## 3. Обов'язкові умови до canonical integration

### I-01 — повний diff

Підготувати окремі повні інтеграційні редакції W23′ і W30. Для кожної заміни навести старий і новий текст, точні секції та перелік залежних посилань. Не застосовувати приховані глобальні replace.

### I-02 — метрика

У W23′.3.2 вже існує `d_F`. Інтеграційний текст повинен або явно визначити `d_P` для PartialTree∞, або встановити, що це окреме розширення тієї самої конструкції першої відмінності. Не перейменовувати `d_F` глобально.

### I-03 — межа

В усіх формулах нового partial layer використовувати `∂_P`, доки не буде доведено сумісність із legacy boundary notation. Перевірити root Leaf, root Node та ABSENT child.

### I-04 — T-007P

Потрібен повний доказ:
`d_H(∂_P p,∂_P q)≤2d_P(p,q)`
для `p,q∈Tω_P^+`. Він має охоплювати випадки першої розбіжності ABSENT/INTERNAL, LEAF/INTERNAL та INTERNAL/INTERNAL. До цього T-007P лишається PROOF REQUIRED і не входить до переліку PROVED.

### I-05 — theorem registry

T-001P та T-006P мають бути записані як окремі твердження з явними залежностями. Уточнити, що T-006P включає компактність `∂_P p` як замкненої множини в компактному Σ_b. Уникати дублювання вже наявних теорем.

### I-06 — proof status

Відокремити:
- аналітичний proof sketch;
- завершене аналітичне доведення;
- чисельний тест;
- Lean kernel proof;
- implementation verification.

Жоден статус не виводиться з іншого автоматично.

## 4. Результат перевірки

| Компонент | Вердикт |
|---|---|
| Архітектура типів | PASS |
| All/rooted code-space design | PASS WITH CONDITIONS |
| Enc/Dec statement | PASS AS PROOF SKETCH |
| Metric transport | PASS AS PROOF SKETCH |
| Partial boundary definition | PASS |
| Tω_P / Tω_P⁺ separation | PASS |
| T-007P | PROOF REQUIRED |
| W23′ full diff | NOT PRODUCED |
| W30 full diff | NOT PRODUCED |
| Canonical files changed | NO |
| Lean verification | NOT EXECUTED |
| W20 regression | NOT EXECUTED |

## 5. Наступний безпечний крок

Створити W23′ інтеграційний кандидат як окремий файл; незалежно звірити його з повним W23′. Потім створити W30 інтеграційний кандидат і провести аналогічну перевірку. Лише після цього можна виконувати canonical updates.

**Висновок:** W34.1.7 отримує CONDITIONAL PASS як інтеграційна пропозиція. Це не означає, що канон уже інтегровано або що SUBIT-WARP v0.4 готовий до STABLE.

**DO NOT COLLAPSE — CONTEXTUALIZE.**
