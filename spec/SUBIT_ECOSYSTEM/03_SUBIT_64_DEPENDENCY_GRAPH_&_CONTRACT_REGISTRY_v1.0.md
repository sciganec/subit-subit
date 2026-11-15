# SUBIT-64 DEPENDENCY GRAPH & CONTRACT REGISTRY
## Version 1.0 — Architecture Specification

**Статус:** ARCHITECTURE DRAFT  
**Система:** SUBIT-ECOSYSTEM  
**Базова архітектура:** SUBIT-64  
**Пов'язаний документ:** SUBIT-64 MODULE INTERDEPENDENCY & CROSS-MODULE MATRIX v1.0  
**Принцип:** DO NOT COLLAPSE — CONTEXTUALIZE

---

# 0. ABSTRACT

Цей документ визначає формальну архітектуру залежностей і міжмодульних контрактів SUBIT-64.

Його мета — перетворити загальну матрицю взаємозалежностей на систему, у якій:

1. Кожен модуль має стабільний ідентифікатор.
2. Кожна залежність має визначений тип і напрямок.
3. Кожен модуль декларує власні інтерфейси.
4. Кожен міжмодульний обмін відбувається через формалізований контракт.
5. Зміни одного модуля не повинні непомітно руйнувати інші.
6. Контекст, походження та причинність інформації зберігаються під час її передавання.
7. Верифікація залежностей відокремлюється від їхнього декларативного опису.

Головне архітектурне положення:

**Модуль не визначається лише тим, що він робить. Він визначається також тим, які відмінності він зберігає, які контракти надає та в якому контексті його результати мають значення.**

---

# 1. SCOPE AND ARCHITECTURAL POSITION

SUBIT-64 Dependency Graph & Contract Registry є інфраструктурним документом для всього SUBIT-ECOSYSTEM.

Він не замінює специфікації окремих модулів.

Його функція — встановити спільний архітектурний рівень, який пов'язує:

- філософські та онтологічні модулі;
- логічні й математичні модулі;
- інформаційні та кібернетичні модулі;
- природничо-наукові моделі;
- обчислювальну інфраструктуру;
- штучний інтелект;
- автономні прикладні системи;
- системи верифікації;
- метатеоретичні та нескінченновимірні структури.

Формально:

G_SUBIT = (V, E, C, I, P, Ω)

де:

- V — множина модулів;
- E — множина типізованих залежностей;
- C — множина контрактів;
- I — множина інтерфейсів;
- P — множина правил походження інформації;
- Ω — множина контекстних станів.

Граф не є просто схемою програмних викликів.

Він описує структурні, семантичні, інформаційні та операційні відносини між модулями.

---

# 2. CANONICAL MODULE IDENTITY

## 2.1. Незмінність ідентифікатора

Кожен модуль отримує стабільний ідентифікатор:

SUBIT-MODULE-ID = Mxx

де xx — двозначний номер від 01 до 64.

Наприклад:

M01 = SUBIT-ONTOLOGY  
M02 = SUBIT-EPISTEMOLOGY  
M33 = SUBIT-CORE  
M37 = SUBIT-CPU  
M41 = SUBIT-CHESS  
M50 = SUBIT-WARP

Ідентифікатор не змінюється внаслідок:

- перейменування модуля;
- зміни реалізації;
- перенесення репозиторію;
- зміни мови програмування;
- реорганізації внутрішніх компонентів.

Якщо модуль розділяється на декілька незалежних модулів, нові модулі отримують нові ідентифікатори, а попередній ідентифікатор зберігається в історії походження.

## 2.2. Розділення ідентичності та назви

Необхідно розрізняти:

Module ID  
Module Name  
Module Version  
Module Specification  
Module Implementation

Наприклад:

```yaml
module_id: M37
module_name: SUBIT-CPU
module_version: 1.0.0
specification_version: 1.0
implementation_version: null
implementation_status: NOT_VERIFIED
```

Назва може змінитися. Ідентичність — ні.

## 2.3. Зв'язок із SUBIT-64

Кожен модуль може мати координатне представлення:

WHO × WHERE × WHEN

Але необхідно розділяти:

- ідентифікатор модуля;
- координатний стан SUBIT-64;
- внутрішній стан модуля;
- версію модуля.

Вони не є взаємозамінними.

Зокрема:

M37 ≠ SUBIT-STATE-37

Номер модуля не повинен автоматично трактуватися як код стану.

Координати WHO, WHERE, WHEN призначаються лише відповідно до канонічної специфікації SUBIT-64.

---

# 3. MODULE REGISTRY

## 3.1. Попередній каталог 64 модулів

Наведений нижче каталог є робочою структурою реєстру.

Позначення:

- CANONICAL-CANDIDATE — назва присутня в попередньо відновленій структурі, але потребує остаточної звірки з Master Technical Specification.
- PROVISIONAL — робоча назва, запропонована для архітектурної організації.
- CONFIRMED — підтверджена назва після звірки з канонічним документом.

До завершення звірки жодна назва не повинна автоматично отримувати статус CONFIRMED.

### GROUP A — FOUNDATIONAL AND PHILOSOPHICAL MODULES

| ID | Module | Registry status |
|---|---|---|
| M01 | SUBIT-ONTOLOGY | CANONICAL-CANDIDATE |
| M02 | SUBIT-EPISTEMOLOGY | CANONICAL-CANDIDATE |
| M03 | SUBIT-PHENOMENOLOGY | CANONICAL-CANDIDATE |
| M04 | SUBIT-SELF-REFERENCE | CANONICAL-CANDIDATE |
| M05 | SUBIT-I-CHING | CANONICAL-CANDIDATE |
| M06 | SUBIT-JUNG | CANONICAL-CANDIDATE |
| M07 | SUBIT-PEIRCE | CANONICAL-CANDIDATE |
| M08 | SUBIT-COGNITION | CANONICAL-CANDIDATE |
| M09 | SUBIT-LOGIC | CANONICAL-CANDIDATE |
| M10 | SUBIT-MATHEMATICS | CANONICAL-CANDIDATE |
| M11 | SUBIT-INFORMATION | CANONICAL-CANDIDATE |
| M12 | SUBIT-CYBERNETICS | CANONICAL-CANDIDATE |
| M13 | SUBIT-TIME | CANONICAL-CANDIDATE |
| M14 | SUBIT-QUANTUM-FOUNDATIONS | CANONICAL-CANDIDATE |
| M15 | SUBIT-QUANTUM-CALCULUS | CANONICAL-CANDIDATE |
| M16 | SUBIT-META-MATHEMATICS | CANONICAL-CANDIDATE |

### GROUP B — SYSTEMS AND NATURAL STRUCTURES

| ID | Module | Registry status |
|---|---|---|
| M17 | SUBIT-SYSTEMS | PROVISIONAL |
| M18 | SUBIT-RELATIONS | PROVISIONAL |
| M19 | SUBIT-GRAPH-THEORY | PROVISIONAL |
| M20 | SUBIT-TOPOLOGY | PROVISIONAL |
| M21 | SUBIT-GEOMETRY | PROVISIONAL |
| M22 | SUBIT-MEASURE-THEORY | PROVISIONAL |
| M23 | SUBIT-DYNAMICS | PROVISIONAL |
| M24 | SUBIT-THERMODYNAMICS | PROVISIONAL |
| M25 | SUBIT-COMPLEXITY | PROVISIONAL |
| M26 | SUBIT-EMERGENCE | PROVISIONAL |
| M27 | SUBIT-BIO | PROVISIONAL |
| M28 | SUBIT-METAMORPHOGENESIS | PROVISIONAL |
| M29 | SUBIT-MORPHOGENESIS | PROVISIONAL |
| M30 | SUBIT-LIPIDOME | PROVISIONAL |
| M31 | SUBIT-ENACTIVISM | PROVISIONAL |
| M32 | SUBIT-COEVOLUTION | PROVISIONAL |

### GROUP C — COMPUTATIONAL AND OPERATIONAL MODULES

| ID | Module | Registry status |
|---|---|---|
| M33 | SUBIT-CORE | PROVISIONAL |
| M34 | SUBIT-LANG | PROVISIONAL |
| M35 | SUBIT-DATA | PROVISIONAL |
| M36 | SUBIT-RUNTIME | PROVISIONAL |
| M37 | SUBIT-CPU | PROVISIONAL |
| M38 | SUBIT-AI | PROVISIONAL |
| M39 | SUBIT-TOOLS | PROVISIONAL |
| M40 | SUBIT-VERIFICATION | PROVISIONAL |
| M41 | SUBIT-CHESS | PROVISIONAL |
| M42 | SUBIT-CPU-ISA | PROVISIONAL |
| M43 | SUBIT-ENGINE | PROVISIONAL |
| M44 | SUBIT-LEARNING | PROVISIONAL |
| M45 | SUBIT-REASONING | PROVISIONAL |
| M46 | SUBIT-MEMORY | PROVISIONAL |
| M47 | SUBIT-AGENTS | PROVISIONAL |
| M48 | SUBIT-INTEROPERABILITY | PROVISIONAL |

### GROUP D — META-ARCHITECTURE AND ADVANCED SYSTEMS

| ID | Module | Registry status |
|---|---|---|
| M49 | SUBIT-INFINITY | PROVISIONAL |
| M50 | SUBIT-WARP | PROVISIONAL |
| M51 | SUBIT-TOPOS | PROVISIONAL |
| M52 | SUBIT-CELESTIAL-HOLOGRAPHY | PROVISIONAL |
| M53 | SUBIT-CHESS-META | PROVISIONAL |
| M54 | SUBIT-QUANTUM-INFORMATION | PROVISIONAL |
| M55 | SUBIT-QUANTUM-OPERATORS | PROVISIONAL |
| M56 | SUBIT-CAUSALITY | PROVISIONAL |
| M57 | SUBIT-EVOLUTION | PROVISIONAL |
| M58 | SUBIT-LINGUA | PROVISIONAL |
| M59 | SUBIT-INK | PROVISIONAL |
| M60 | SUBIT-CHESS-ANALYSIS | PROVISIONAL |
| M61 | SUBIT-SECURITY | PROVISIONAL |
| M62 | SUBIT-GOVERNANCE | PROVISIONAL |
| M63 | SUBIT-CONFORMANCE | PROVISIONAL |
| M64 | SUBIT-VERIFICATION-INFINITY | PROVISIONAL |

**Критичне застереження:** цей каталог не є затвердженим канонічним переліком SUBIT-64. Його призначення — надати повну робочу сітку для побудови реєстру. Перед фіксацією ID необхідно звірити всі 64 назви з канонічним Master Technical Specification. Не можна мовчки переносити цей перелік у статус остаточного.

---

# 4. DEPENDENCY MODEL

## 4.1. Загальна модель залежності

Залежність між модулями задається орієнтованим типізованим ребром:

e = (Mᵢ, Mⱼ, τ, κ, π)

де:

- Mᵢ — модуль, що оголошує залежність;
- Mⱼ — модуль, від якого залежить Mᵢ;
- τ — тип залежності;
- κ — контракт, через який реалізується залежність;
- π — політика сумісності.

У цьому документі використовується напрямок:

**Mᵢ → Mⱼ означає: Mᵢ залежить від Mⱼ.**

Це принципово важливо.

Граф залежностей не тотожний графу викликів.

Наприклад:

SUBIT-CPU → SUBIT-CORE

означає, що CPU залежить від типів і контрактів CORE.

Це не означає, що CORE викликає CPU.

## 4.2. Типи залежностей

Визначаються такі типи:

| Type | Meaning |
|---|---|
| FND | Foundational dependency |
| API | Interface dependency |
| DATA | Data-schema dependency |
| SEM | Semantic dependency |
| EVT | Event dependency |
| VER | Verification dependency |
| EXT | Extension dependency |
| OPT | Optional dependency |
| REF | Reference-only dependency |

### FND — Foundational

Модуль не може коректно існувати без фундаментальних визначень іншого модуля.

### API — Interface

Модуль використовує формально визначений інтерфейс іншого модуля.

### DATA — Data

Модуль залежить від структури даних або схеми.

### SEM — Semantic

Модуль використовує семантичні визначення іншого модуля.

### EVT — Event

Модуль споживає або породжує події, визначені контрактом іншого модуля.

### VER — Verification

Модуль підлягає правилам або процедурам верифікації іншого модуля.

### EXT — Extension

Модуль розширює функціональність іншого модуля, не змінюючи його фундаментальних контрактів.

### OPT — Optional

Залежність може бути відсутньою без втрати базової функціональності.

### REF — Reference

Модуль посилається на концепції іншого модуля, але не використовує їх як обов'язкову операційну залежність.

---

# 5. CONTRACT MODEL

## 5.1. Що таке контракт SUBIT

Контракт — формалізована угода між двома або більше модулями.

Він визначає:

- що модуль надає;
- що модуль очікує;
- які типи даних використовуються;
- які контексти є допустимими;
- які обмеження діють;
- які гарантії надаються;
- як перевіряється сумісність.

Контракт не повинен залежати від конкретної реалізації.

Формально:

C = (ID, Provider, Consumer, Inputs, Outputs, Preconditions, Postconditions, Invariants, Version)

## 5.2. Контракт не є просто API

API описує спосіб взаємодії.

Контракт описує допустимість і значення цієї взаємодії.

Отже:

API ⊂ Contract

API може бути реалізований як:

- функціональний виклик;
- повідомлення;
- подія;
- файл;
- потоковий інтерфейс;
- локальний протокол;
- формальна математична структура.

Але контракт повинен залишатися семантично стабільним незалежно від транспортного механізму.

## 5.3. Структура контракту

Кожен контракт повинен мати такі поля:

```yaml
contract_id: C-CORE-001

contract_name: CanonicalEntityContract

provider:
  module_id: M33
  module_name: SUBIT-CORE

consumers:
  - M35
  - M36
  - M37
  - M38

version: 1.0.0

interface_type: DATA_AND_SEMANTIC

inputs:
  - entity_id
  - entity_type
  - context_ref
  - provenance_ref

outputs:
  - canonical_entity

preconditions:
  - entity_id_is_valid
  - entity_type_is_registered

postconditions:
  - entity_identity_is_preserved
  - context_is_preserved
  - provenance_is_preserved

invariants:
  - no_silent_context_collapse
  - no_implicit_identity_conversion

compatibility:
  policy: SEMVER

verification:
  required: true
  status: SPECIFIED_NOT_VERIFIED
```

---

# 6. CANONICAL CONTRACT REGISTRY

Перший набір контрактів визначається для восьми центральних технічних модулів.

## C-CORE-001 — Canonical Entity Contract

**Provider:** SUBIT-CORE  
**Consumers:** SUBIT-DATA, SUBIT-RUNTIME, SUBIT-CPU, SUBIT-AI

Визначає канонічну структуру сутності.

Entity:

```text
Entity = (
    entity_id,
    entity_type,
    state,
    context_ref,
    provenance_ref,
    revision
)
```

Інваріанти:

1. entity_id стабільний.
2. entity_type визначений.
3. state має типізоване представлення.
4. context_ref не може бути непомітно видалений.
5. provenance_ref не може бути непомітно видалений.
6. revision змінюється за визначеними правилами.

## C-CORE-002 — Canonical Event Contract

**Provider:** SUBIT-CORE  
**Consumers:** SUBIT-DATA, SUBIT-LANG, SUBIT-RUNTIME, SUBIT-CPU, SUBIT-AI

Event:

```text
Event = (
    event_id,
    entity_ref,
    event_type,
    payload,
    context_ref,
    provenance_ref,
    timestamp,
    causality_ref
)
```

Основні правила:

- Event є незмінним після фіксації.
- Виправлення події створює нову подію.
- Порядок подій не можна виводити лише з локального часу.
- Причинність не можна ототожнювати з часовою послідовністю.
- Повторне отримання тієї самої події не повинно спричиняти повторне застосування її ефекту.

## C-CORE-003 — Context Contract

**Provider:** SUBIT-CORE  
**Consumers:** усі модулі, що працюють із контекстно залежними даними.

Context:

```text
Context = (
    context_id,
    scope,
    environment,
    conditions,
    perspective,
    temporal_scope
)
```

Контракт вимагає зберігати умови, у яких твердження, стан або подія мають значення.

Контекст не є довільним коментарем.

Він є структурним компонентом інформації.

## C-CORE-004 — Provenance Contract

**Provider:** SUBIT-CORE  
**Consumers:** DATA, AI, TOOLS, VERIFICATION.

Provenance:

```text
Provenance = (
    provenance_id,
    origin,
    author,
    source,
    method,
    timestamp,
    evidence_ref
)
```

Забороняється перетворювати результат моделі на твердження про зовнішній факт без зазначення його походження та способу отримання.

## C-LANG-001 — Typed Event Schema Contract

**Provider:** SUBIT-LANG  
**Consumers:** SUBIT-RUNTIME, SUBIT-CPU, SUBIT-AI, SUBIT-TOOLS.

Контракт визначає:

- структуру подій;
- типи полів;
- правила серіалізації;
- допустимі версії схем;
- правила перевірки;
- правила міграції.

Мова не повинна непомітно змінювати значення даних під час перетворення.

## C-DATA-001 — Event Store Contract

**Provider:** SUBIT-DATA  
**Consumers:** SUBIT-RUNTIME, SUBIT-CPU, SUBIT-AI, SUBIT-TOOLS.

Гарантії:

- append-only запис подій;
- контроль унікальності event_id;
- відтворення послідовності;
- перевірка цілісності;
- збереження provenance;
- контроль версій схем.

Event Store не повинен самостійно інтерпретувати семантику подій.

Це відповідальність відповідного reducer або семантичного компонента.

## C-RUNTIME-001 — Execution Contract

**Provider:** SUBIT-RUNTIME  
**Consumers:** SUBIT-CPU, SUBIT-AI, SUBIT-TOOLS.

Визначає правила виконання:

- перевірка вхідних даних;
- контроль дозволів;
- керування транзакціями;
- обмеження ресурсів;
- обробка помилок;
- повторне виконання;
- журналювання;
- фіксація результатів.

## C-CPU-001 — Computational Operation Contract

**Provider:** SUBIT-CPU  
**Consumers:** SUBIT-CHESS, SUBIT-ENGINE, SUBIT-AI та інші обчислювальні модулі.

Визначає допустимі операції, їхні типи, результати та обмеження.

Базові операції SUBIT-CPU:

```text
NOT
AND
OR
XOR
ROTATE
MERGE
SJOIN
SMEET
```

Операції повинні зберігати відмінність між:

- координатним станом SUBIT-64;
- чотиризначною логікою Belnap/Dunn FOUR;
- звичайними числовими значеннями;
- станами виконання.

## C-VERIFICATION-001 — Verification Evidence Contract

**Provider:** SUBIT-VERIFICATION  
**Consumers:** усі модулі, що заявляють про перевірені властивості.

Результат перевірки:

```text
VerificationResult = (
    verification_id,
    subject_ref,
    claim,
    method,
    environment,
    evidence_ref,
    status,
    timestamp
)
```

Допустимі статуси:

```text
NOT_SPECIFIED
SPECIFIED
IMPLEMENTED
TESTED
VERIFIED
FAILED
BLOCKED
```

Статуси не є синонімами.

Наприклад:

SPECIFIED ≠ IMPLEMENTED  
IMPLEMENTED ≠ TESTED  
TESTED ≠ VERIFIED

Формальна верифікація повинна посилатися на відтворюваний доказ або процедуру перевірки.

---

# 7. CORE DEPENDENCY GRAPH

## 7.1. Базова залежність

Центральна група технічних модулів:

- M33 SUBIT-CORE
- M34 SUBIT-LANG
- M35 SUBIT-DATA
- M36 SUBIT-RUNTIME
- M37 SUBIT-CPU
- M38 SUBIT-AI
- M39 SUBIT-TOOLS
- M40 SUBIT-VERIFICATION

Залежності:

```text
SUBIT-LANG
    → SUBIT-CORE

SUBIT-DATA
    → SUBIT-CORE

SUBIT-RUNTIME
    → SUBIT-CORE
    → SUBIT-LANG
    → SUBIT-DATA

SUBIT-CPU
    → SUBIT-CORE
    → SUBIT-DATA
    → SUBIT-RUNTIME

SUBIT-AI
    → SUBIT-CORE
    → SUBIT-LANG
    → SUBIT-DATA
    → SUBIT-RUNTIME

SUBIT-TOOLS
    → SUBIT-CORE
    → SUBIT-DATA
    → SUBIT-RUNTIME

SUBIT-VERIFICATION
    → SUBIT-CORE
    → SUBIT-LANG
    → SUBIT-DATA
    → SUBIT-RUNTIME
```

Це початкова модель залежностей, а не повний граф викликів.

## 7.2. Архітектурні обмеження

**RULE-DEP-001**

SUBIT-CORE не повинен залежати від прикладних модулів.

**RULE-DEP-002**

SUBIT-CORE не повинен залежати від SUBIT-AI.

**RULE-DEP-003**

SUBIT-DATA не повинен самостійно визначати семантичне значення подій.

**RULE-DEP-004**

SUBIT-CPU не повинен обходити контракти CORE і DATA для запису системних подій.

**RULE-DEP-005**

SUBIT-VERIFICATION не повинен змінювати об'єкт, який перевіряє, без окремого контракту на таку операцію.

**RULE-DEP-006**

Прикладні модулі не повинні безпосередньо залежати від внутрішньої реалізації інших прикладних модулів.

**RULE-DEP-007**

Залежність від реалізації заборонена там, де достатньо залежності від контракту.

---

# 8. DEPENDENCY CYCLES

## 8.1. Проблема циклів

Цикл у графі залежностей не завжди є помилкою.

Наприклад, два модулі можуть обмінюватися подіями через асинхронний протокол.

Але цикл фундаментальних залежностей може зробити архітектуру нерозв'язною.

Тому визначаються два рівні графа:

G_FND — граф фундаментальних залежностей.

G_RUNTIME — граф операційних взаємодій.

## 8.2. Обмеження

Для G_FND:

```text
G_FND MUST BE ACYCLIC
```

Для G_RUNTIME:

```text
CYCLES ARE ALLOWED
IF:
    protocol_is_declared
    termination_or_liveness_is_defined
    state_transition_is_bounded_or_monitored
    failure_handling_is_defined
```

## 8.3. Перевірка

Для кожного циклу G_RUNTIME необхідно визначити:

- тип циклу;
- його призначення;
- механізм завершення;
- умови повтору;
- захист від нескінченного повторення;
- правила відновлення після помилки.

Особливо важливо для:

- AI ↔ RUNTIME;
- CPU ↔ DATA;
- AGENTS ↔ TOOLS;
- CHESS ↔ ENGINE;
- CHESS-META ↔ CHESS.

---

# 9. CONTEXT AND PROVENANCE PROPAGATION

## 9.1. Загальне правило

Кожне міжмодульне повідомлення повинно мати визначену політику контексту та походження.

Формально:

Transfer(x, Mᵢ, Mⱼ) →

(x, Context(x), Provenance(x), Causality(x))

Якщо частина інформації не застосовується, це повинно бути виражено явно.

Відсутність контексту не повинна автоматично означати, що контекст не має значення.

## 9.2. Заборонене перетворення

```text
Input:
    x + Context + Provenance

Unsafe transformation:
    x

Result:
    Context lost
    Provenance lost
```

Таке перетворення є порушенням інваріанта.

## 9.3. Дозволене перетворення

```text
Input:
    x + Context + Provenance

Transformation:
    f(x, Context)

Output:
    y + Context' + Provenance'
```

При цьому Provenance' повинен містити посилання на попереднє походження.

Контекст може змінитися, але його трансформація повинна бути задокументована.

---

# 10. CONTRACT COMPATIBILITY

## 10.1. Версіонування

Використовується схема:

MAJOR.MINOR.PATCH

### PATCH

- виправлення помилок;
- уточнення документації;
- внутрішні зміни без зміни контракту.

### MINOR

- нові необов'язкові поля;
- нові сумісні операції;
- розширення допустимих значень за умови збереження старої семантики.

### MAJOR

- зміна типів;
- зміна семантики;
- вилучення полів;
- зміна обов'язкових передумов;
- несумісні зміни поведінки.

## 10.2. Compatibility Matrix

Для кожної пари версій:

```text
Compatibility(
    ProviderVersion,
    ConsumerVersion,
    ContractVersion
)
```

Результат:

```text
COMPATIBLE
COMPATIBLE_WITH_ADAPTER
INCOMPATIBLE
UNKNOWN
```

UNKNOWN не можна трактувати як COMPATIBLE.

## 10.3. Адаптери

Якщо новий контракт несумісний зі старим, допускається адаптер.

Адаптер повинен:

- мати власний ID;
- мати версію;
- описувати трансформацію;
- зберігати provenance;
- зберігати контекст;
- визначати втрати інформації;
- мати власні тести.

Адаптер не повинен приховувати семантичну несумісність.

---

# 11. MACHINE-READABLE REGISTRY

Для автоматизації реєстр повинен мати машинозчитуване представлення.

Рекомендований початковий формат — YAML.

```yaml
registry:
  name: SUBIT-64
  version: 1.0.0
  status: ARCHITECTURE_DRAFT

principle:
  - DO_NOT_COLLAPSE
  - CONTEXTUALIZE

module_id_policy:
  format: Mxx
  immutable: true
  range:
    min: 1
    max: 64

dependency_policy:
  direction: consumer_to_provider
  foundational_graph:
    must_be_acyclic: true

contract_policy:
  versioning: SEMVER
  require_provenance: true
  require_context: true

modules:
  - module_id: M33
    name: SUBIT-CORE
    status: PROVISIONAL
    contracts:
      provides:
        - C-CORE-001
        - C-CORE-002
        - C-CORE-003
        - C-CORE-004
      consumes: []

  - module_id: M35
    name: SUBIT-DATA
    status: PROVISIONAL
    dependencies:
      - module_id: M33
        type: FND
    contracts:
      provides:
        - C-DATA-001
      consumes:
        - C-CORE-001
        - C-CORE-002

  - module_id: M37
    name: SUBIT-CPU
    status: PROVISIONAL
    dependencies:
      - module_id: M33
        type: FND
      - module_id: M35
        type: DATA
      - module_id: M36
        type: API
    contracts:
      provides:
        - C-CPU-001
      consumes:
        - C-CORE-001
        - C-CORE-002
        - C-DATA-001
```

Цей фрагмент є прикладом схеми, а не завершеним реєстром усіх 64 модулів.

---

# 12. REGISTRY VALIDATION

Реєстр повинен проходити такі перевірки.

## REG-001 — Unique IDs

Усі module_id унікальні.

## REG-002 — ID Stability

Ідентифікатор не змінюється при перейменуванні.

## REG-003 — Valid Dependencies

Кожна залежність посилається на зареєстрований модуль.

## REG-004 — Valid Contract References

Кожне посилання на контракт має існувати.

## REG-005 — Provider Consistency

Кожен контракт має одного визначеного провайдера або явно задекларовану множину провайдерів.

## REG-006 — Dependency Direction

Напрямок залежності відповідає правилу consumer → provider.

## REG-007 — Foundational Acyclicity

G_FND не містить циклів.

## REG-008 — Context Preservation

Кожен контракт, який передає контекстно залежні дані, декларує правила його збереження.

## REG-009 — Provenance Preservation

Кожен контракт, який передає твердження, дані або результати обчислення, визначає походження.

## REG-010 — Version Compatibility

Несумісні версії не позначаються як сумісні без адаптера.

## REG-011 — Verification Status

Статус VERIFIED допускається лише за наявності відповідного доказу.

## REG-012 — No Implicit Equivalence

Різні типи станів не об'єднуються без явного правила перетворення.

---

# 13. SUBIT-CHESS AS A CONTRACTED APPLICATION

SUBIT-CHESS використовується як приклад застосування реєстру.

Він повинен залишатися автономним шаховим двигуном.

Його архітектура не повинна залежати від сторонніх шахових двигунів, стороннього коду чи зовнішніх партійних баз як джерела навчання.

Його рішення повинні випливати з власного аналізу позиції, легальних перетворень і наслідків ходів.

## 13.1. Основні залежності

```text
SUBIT-CHESS
    → SUBIT-CORE
    → SUBIT-CPU
    → SUBIT-ENGINE
    → SUBIT-REASONING
    → SUBIT-VERIFICATION
```

Конкретні залежності мають бути уточнені після фіксації окремих контрактів цих модулів.

## 13.2. Контракт позиції

C-CHESS-001:

```text
ChessPosition = (
    position_id,
    board_state,
    side_to_move,
    castling_rights,
    en_passant_state,
    halfmove_clock,
    fullmove_number,
    context_ref,
    provenance_ref
)
```

## 13.3. Контракт легального ходу

C-CHESS-002:

```text
LegalMove = (
    move_id,
    source_square,
    target_square,
    promotion,
    precondition,
    resulting_position
)
```

Легальність ходу повинна бути визначена правилами шахів, а не оцінкою AI.

## 13.4. Контракт оцінки позиції

C-CHESS-003:

```text
PositionEvaluation = (
    position_ref,
    evaluation_value,
    evaluation_basis,
    structural_features,
    candidate_moves,
    search_context,
    provenance_ref
)
```

Оцінка повинна дозволяти відрізнити:

- факт легальності ходу;
- евристичну оцінку;
- результат пошуку;
- стратегічне припущення;
- підтверджений результат аналізу.

## 13.5. Самовдосконалення

C-CHESS-004:

Навчальні або оптимізаційні процеси повинні використовувати:

- самостійно згенеровані позиції;
- власні результати пошуку;
- self-play;
- незалежну валідацію;
- контроль регресій.

Результат навчання не повинен автоматично ставати доведеним знанням.

Він є новою версією моделі або евристики, яка потребує перевірки.

---

# 14. GOVERNANCE AND CHANGE CONTROL

Кожна зміна реєстру повинна мати:

```text
ChangeRequest = (
    change_id,
    affected_modules,
    affected_contracts,
    reason,
    proposed_change,
    compatibility_impact,
    verification_plan,
    approval_status
)
```

Зміна класифікується як:

- MODULE_ADDITION;
- MODULE_REMOVAL;
- MODULE_RENAME;
- CONTRACT_CHANGE;
- DEPENDENCY_CHANGE;
- SEMANTIC_CHANGE;
- VERSION_CHANGE;
- VERIFICATION_CHANGE.

## 14.1. Заборона непомітної зміни

Якщо зміна контракту впливає на інший модуль, реєстр повинен показати цей вплив.

Не допускається:

- видалення залежності без перевірки споживачів;
- зміна семантики без підвищення версії;
- перейменування ID;
- автоматичне прирівнювання невідомого статусу до успішного;
- втрата історії контракту.

## 14.2. Impact Analysis

Для зміни модуля Mᵢ:

Impact(Mᵢ) = DirectConsumers(Mᵢ) ∪ TransitiveConsumers(Mᵢ)

Це дає змогу визначити, які модулі можуть бути зачеплені зміною провайдера.

Однак транзитивний вплив не означає, що кожен модуль обов'язково потребує зміни. Він означає, що кожен потенційно зачеплений контракт має бути перевірений.

---

# 15. ACCEPTANCE CRITERIA

Версія 1.0 вважається архітектурно завершеною після виконання таких умов:

- AC-001: визначено стабільну модель Module ID;
- AC-002: зафіксовано напрямок ребер графа;
- AC-003: визначено типи залежностей;
- AC-004: визначено структуру контракту;
- AC-005: створено реєстр центральних контрактів;
- AC-006: розділено G_FND та G_RUNTIME;
- AC-007: встановлено правило ациклічності фундаментального графа;
- AC-008: визначено правила контексту;
- AC-009: визначено правила provenance;
- AC-010: визначено версіонування;
- AC-011: визначено правила сумісності;
- AC-012: визначено перевірки реєстру;
- AC-013: визначено правила управління змінами;
- AC-014: створено приклад застосування для SUBIT-CHESS;
- AC-015: усі непідтверджені назви модулів явно позначено.

**Статус перевірки:** SPECIFICATION COMPLETE AS DRAFT.  
**Реалізація:** NOT VERIFIED.  
**Автоматичне проходження тестів:** NOT CLAIMED.

---

# 16. OPEN QUESTIONS

Перед переходом до реалізації необхідно вирішити такі питання.

### Q-001. Канонічний каталог

Чи відповідає наведена робоча структура 64 модулів останній редакції Master Technical Specification?

До остаточного підтвердження не можна фіксувати її як канон.

### Q-002. Координатна прив'язка

Чи має кожен модуль одну основну координату SUBIT-64, чи може модуль мати декілька контекстно залежних координат?

Необхідно не допустити ототожнення координатного стану та ідентичності модуля.

### Q-003. Семантичні контракти

Чи повинні філософські, математичні та природничі модулі мати такі самі машинозчитувані контракти, як програмні модулі?

Попередня відповідь: так, але рівень формалізації має залежати від природи тверджень.

### Q-004. Формат реєстру

Чи буде YAML основним джерелом реєстру, а JSON — похідним форматом для машинної обробки?

Попередня рекомендація: YAML як основний декларативний формат, JSON як сумісне машинозчитуване представлення.

### Q-005. Перевірка контрактів

Чи буде SUBIT-VERIFICATION окремим модулем, чи центральною підсистемою з перевірочними компонентами в кожному модулі?

Попередня рекомендація: розподілені локальні перевірки плюс центральний реєстр доказів.

---

# 17. NEXT DEVELOPMENT STAGE

Наступний документ:

**SUBIT-64 CROSS-MODULE CONTRACT PROTOCOL & EVENT EXCHANGE SPECIFICATION v1.0**

Він повинен визначити:

1. Протокол передавання даних між модулями.
2. Канонічний формат міжмодульних повідомлень.
3. Систему Event Envelope.
4. Контекстне та provenance-збагачення повідомлень.
5. Ідемпотентність і повторне доставлення.
6. Версіонування схем.
7. Синхронні та асинхронні взаємодії.
8. Обробку конфліктів.
9. Межі транзакцій.
10. Відновлення після помилок.
11. Протокол міжмодульної верифікації.

Головний принцип наступного етапу:

**Модулі повинні обмінюватися не просто значеннями, а типізованими повідомленнями, які зберігають ідентичність, контекст, походження та причинну історію.**

---

# 18. FINAL ARCHITECTURAL STATEMENT

SUBIT-64 Dependency Graph & Contract Registry встановлює важливу відмінність між архітектурною єдністю та механічною централізацією.

Єдність системи не означає, що всі модулі повинні мати однакову структуру, використовувати однакові методи або підпорядковуватися одному операційному механізму.

Єдність виникає через сумісність відмінностей.

Модуль зберігає власну функцію, семантику та контекст, але водночас може брати участь у загальній системі через чітко визначені контракти.

Тому:

SUBIT-ECOSYSTEM ≠ SUM OF MODULES

SUBIT-ECOSYSTEM = MODULES + RELATIONS + CONTRACTS + CONTEXT + PROVENANCE + DYNAMICS

Архітектурна цілісність полягає не в усуненні відмінностей, а в тому, щоб зробити їх сумісними без втрати їхнього значення.

**DO NOT COLLAPSE — CONTEXTUALIZE.**