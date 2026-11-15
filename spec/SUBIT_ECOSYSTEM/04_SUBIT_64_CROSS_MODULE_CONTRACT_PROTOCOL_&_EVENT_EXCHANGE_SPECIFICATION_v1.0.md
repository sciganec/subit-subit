# SUBIT-64 CROSS-MODULE CONTRACT PROTOCOL & EVENT EXCHANGE SPECIFICATION

## Version 1.0 — Intermodule Communication Architecture

**Статус:** ARCHITECTURE DRAFT  
**Система:** SUBIT-ECOSYSTEM  
**Базова архітектура:** SUBIT-64  
**Попередні документи:**
- SUBIT-64 MODULE INTERDEPENDENCY & CROSS-MODULE MATRIX v1.0
- SUBIT-64 DEPENDENCY GRAPH & CONTRACT REGISTRY v1.0

**Ключовий принцип:** DO NOT COLLAPSE — CONTEXTUALIZE.

---

# 0. ABSTRACT

SUBIT-64 CROSS-MODULE CONTRACT PROTOCOL визначає єдиний архітектурний протокол взаємодії між модулями SUBIT-ECOSYSTEM.

Його завдання — забезпечити структурно узгоджений обмін:

- даними;
- станами;
- повідомленнями;
- подіями;
- командами;
- результатами обчислень;
- доказами;
- контекстами;
- метаданими походження;
- причинними зв'язками.

Основна проблема міжмодульної архітектури полягає не лише в передаванні інформації.

Проблема полягає у збереженні її ідентичності та значення під час переходу з одного контексту в інший.

Наприклад, результат SUBIT-AI, переданий до SUBIT-CHESS, не повинен автоматично трактуватися як перевірений факт шахової позиції.

Він повинен зберігати:

1. джерело;
2. метод отримання;
3. контекст;
4. версію моделі;
5. статус перевірки;
6. межі достовірності.

Тому протокол вводить поняття:

**SUBIT EVENT ENVELOPE**

Це канонічна структура міжмодульного повідомлення, яка об'єднує дані, ідентичність, контекст, provenance, причинність і правила обробки.

Головне положення:

**Жодне повідомлення не повинно втрачати структурну інформацію лише тому, що переходить між різними модулями.**

---

# 1. ARCHITECTURAL POSITION

## 1.1. Місце протоколу

Протокол розташовується між контрактами модулів та механізмами виконання.

Архітектурна схема:

```text
SUBIT MODULES
     │
     ▼
MODULE CONTRACTS
     │
     ▼
CROSS-MODULE PROTOCOL
     │
     ├── Message Exchange
     ├── Event Exchange
     ├── Command Exchange
     ├── Context Propagation
     ├── Provenance Propagation
     ├── Causality Tracking
     └── Verification Exchange
     │
     ▼
SUBIT RUNTIME
     │
     ▼
SUBIT DATA / EVENT STORE
```

Ця схема описує логічні ролі, а не обов'язковий порядок фізичного розташування програмних компонентів.

## 1.2. Відмінність між повідомленням, подією та командою

Ці три поняття не можна об'єднувати.

### Message

Повідомлення — інформаційний об'єкт, переданий від одного компонента іншому.

Воно може бути запитом, відповіддю, повідомленням про стан або транспортною оболонкою події.

### Event

Подія — зафіксоване твердження про те, що певна зміна або факт відбулися в конкретному контексті.

Подія описує минуле або вже зафіксоване системне спостереження.

### Command

Команда — запит на виконання певної дії.

Команда сама по собі не доводить, що дія відбулася.

Наприклад:

```text
Command:
    MOVE_PIECE(e2, e4)

Event:
    PIECE_MOVED(e2, e4)

Verification:
    MOVE_LEGALITY_CONFIRMED
```

Ці три об'єкти мають різні семантичні статуси.

---

# 2. PROTOCOL FUNDAMENTALS

## 2.1. Канонічна модель обміну

Кожна міжмодульна взаємодія визначається як:

X = (S, D, T, C, P, K, V)

де:

- S — Source Module;
- D — Destination Module;
- T — Message Type;
- C — Context;
- P — Provenance;
- K — Causality;
- V — Contract Version.

Передавання:

Transfer(X, S, D) → X′

має зберігати ідентичність повідомлення та всі структурні властивості, необхідні для його коректної інтерпретації.

## 2.2. Базові інваріанти

**INV-PROTO-001 — Identity Preservation**

Повідомлення повинно мати стабільний ідентифікатор.

**INV-PROTO-002 — Context Preservation**

Контекст не можна непомітно видаляти.

**INV-PROTO-003 — Provenance Preservation**

Походження даних має бути доступним для подальшої перевірки.

**INV-PROTO-004 — Causality Preservation**

Причинні зв'язки повинні передаватися явно.

**INV-PROTO-005 — Type Safety**

Повідомлення повинно відповідати заявленій схемі.

**INV-PROTO-006 — Version Awareness**

Одержувач повинен знати версію контракту.

**INV-PROTO-007 — No Semantic Inflation**

Результат із невизначеним статусом не може автоматично перетворюватися на підтверджений факт.

**INV-PROTO-008 — No Silent Transformation**

Будь-яке семантично значуще перетворення повинно бути задокументоване.

**INV-PROTO-009 — Idempotent Processing**

Повторне доставлення одного повідомлення не повинно непомітно створювати повторний ефект.

**INV-PROTO-010 — Explicit Failure**

Помилка передавання або обробки повинна мати визначений статус.

---

# 3. SUBIT EVENT ENVELOPE

## 3.1. Визначення

SUBIT EVENT ENVELOPE — канонічна оболонка міжмодульної взаємодії.

Вона відокремлює:

- транспортну інформацію;
- семантичний вміст;
- контекст;
- provenance;
- причинність;
- політики обробки.

Формально:

Envelope = (H, B, C, P, K, Q)

де:

- H — Header;
- B — Body;
- C — Context;
- P — Provenance;
- K — Causality;
- Q — Processing Metadata.

## 3.2. Header

Header:

```text
Header = (
    message_id,
    message_type,
    source_module,
    destination_module,
    contract_id,
    contract_version,
    schema_version,
    created_at,
    correlation_id,
    causation_id
)
```

Поля:

- message_id — унікальний ідентифікатор повідомлення;
- message_type — тип повідомлення;
- source_module — модуль-відправник;
- destination_module — модуль-одержувач;
- contract_id — контракт, який регулює взаємодію;
- contract_version — версія контракту;
- schema_version — версія схеми;
- created_at — час створення;
- correlation_id — ідентифікатор загальної операції;
- causation_id — ідентифікатор безпосередньої причини.

`correlation_id` дозволяє об'єднувати кілька повідомлень в одну операційну історію.

`causation_id` дозволяє простежити, яке попереднє повідомлення спричинило поточне.

## 3.3. Body

Body містить семантичний вміст повідомлення.

```text
Body = (
    payload_type,
    payload,
    semantic_status
)
```

`payload_type` визначає структуру даних.

`payload` містить фактичний вміст.

`semantic_status` визначає статус твердження або результату.

Приклади:

```text
OBSERVED
COMPUTED
INFERRED
REQUESTED
CONFIRMED
REJECTED
UNKNOWN
```

Ці статуси не є взаємозамінними.

## 3.4. Context

```text
Context = (
    context_id,
    scope,
    environment,
    conditions,
    perspective,
    temporal_scope,
    coordinate_ref
)
```

Контекст визначає умови, у яких payload має значення.

`coordinate_ref` є необов'язковим посиланням на координатне представлення SUBIT-64.

Відсутність `coordinate_ref` не означає, що повідомлення не має контексту.

Координатний стан SUBIT-64 не можна ототожнювати з ідентифікатором модуля або транспортним ідентифікатором повідомлення.

## 3.5. Provenance

```text
Provenance = (
    provenance_id,
    origin_module,
    origin_type,
    author_or_agent,
    method,
    source_refs,
    model_version,
    evidence_refs,
    parent_provenance
)
```

Не всі поля обов'язкові для кожного типу повідомлення.

Наприклад, для повідомлення, створеного детермінованою операцією CPU, поле model_version може бути непридатним.

Але відсутність поля повинна визначатися схемою, а не випадковою втратою даних.

## 3.6. Causality

```text
Causality = (
    causality_id,
    parent_event_ids,
    relation_type,
    causal_order,
    evidence_refs
)
```

Допустимі типи зв'язків:

```text
CAUSES
DERIVES_FROM
TRIGGERS
RESPONDS_TO
CORRECTS
SUPERSEDES
CORRELATES_WITH
```

`CORRELATES_WITH` не означає причинності.

`SUPERSEDES` не означає, що попередня подія ніколи не відбувалася.

## 3.7. Processing Metadata

```text
ProcessingMetadata = (
    delivery_id,
    attempt_number,
    idempotency_key,
    priority,
    deadline,
    delivery_policy,
    acknowledgement_policy
)
```

Ці поля використовуються для керування передаванням.

Вони не повинні змінювати семантичний вміст події.

---

# 4. CANONICAL ENVELOPE EXAMPLE

```yaml
envelope:
  header:
    message_id: msg-000001
    message_type: POSITION_EVALUATED

    source_module: M41
    destination_module: M40

    contract_id: C-CHESS-003
    contract_version: 1.0.0
    schema_version: 1.0

    created_at: "2026-11-14T19:00:00Z"

    correlation_id: chess-analysis-0001
    causation_id: position-created-0001

  body:
    payload_type: PositionEvaluation

    payload:
      position_ref: position-0001
      evaluation_value: 0.42
      evaluation_basis:
        - material_balance
        - king_safety
        - mobility
      candidate_moves:
        - e2e4
        - d2d4

    semantic_status: COMPUTED

  context:
    context_id: chess-context-0001
    scope: chess_position_analysis
    environment: local_engine
    conditions:
      side_to_move: white
      search_depth: 8
    perspective: white_to_move
    temporal_scope: current_position

  provenance:
    provenance_id: provenance-0001
    origin_module: M41
    origin_type: INTERNAL_COMPUTATION
    method: native_position_evaluation
    model_version: null
    source_refs:
      - position-0001
    evidence_refs: []

  causality:
    causality_id: causal-0001
    parent_event_ids:
      - position-created-0001
    relation_type: DERIVES_FROM
    causal_order: 2

  processing:
    delivery_id: delivery-0001
    attempt_number: 1
    idempotency_key: evaluation-position-0001
    delivery_policy: AT_LEAST_ONCE
    acknowledgement_policy: AFTER_ACCEPTANCE
```

Цей приклад ілюструє структуру повідомлення.

Він не означає, що SUBIT-CHESS вже реалізує зазначений протокол.

---

# 5. MESSAGE EXCHANGE PROTOCOL

## 5.1. Типи повідомлень

Визначаються такі класи:

| Class | Purpose |
|---|---|
| REQUEST | Запит на отримання даних або виконання операції |
| RESPONSE | Відповідь на запит |
| COMMAND | Запит на зміну стану |
| EVENT | Повідомлення про зафіксовану подію |
| ACK | Підтвердження прийняття |
| NACK | Відмова у прийнятті |
| ERROR | Повідомлення про помилку |
| VERIFY | Запит або результат перевірки |
| HEARTBEAT | Сигнал доступності компонента |

## 5.2. REQUEST / RESPONSE

Синхронний обмін:

```text
A → REQUEST → B
A ← RESPONSE ← B
```

Запит має містити:

- request_id;
- contract_id;
- payload;
- context;
- deadline;
- correlation_id.

Відповідь повинна містити посилання на request_id.

Забороняється трактувати відсутність відповіді як позитивний результат.

Можливі статуси:

```text
SUCCESS
REJECTED
TIMEOUT
PARTIAL
UNKNOWN
```

## 5.3. COMMAND

Команда описує бажану операцію.

```text
COMMAND
   ↓
VALIDATION
   ↓
EXECUTION
   ↓
COMMIT
   ↓
EVENT
```

Прийняття команди не означає успішного виконання.

Тому:

COMMAND_ACCEPTED ≠ COMMAND_COMPLETED

## 5.4. EVENT

Подія повідомляє про вже зафіксовану зміну.

Подія не повинна бути перезаписана внаслідок зміни поточного стану системи.

Якщо подія виявилася помилковою, створюється окрема коригувальна подія.

---

# 6. SYNCHRONOUS AND ASYNCHRONOUS EXCHANGE

## 6.1. Синхронна взаємодія

Застосовується, коли результат необхідний для продовження поточної операції.

Переваги:

- проста модель запит-відповідь;
- зрозумілий контроль результату;
- зручна локальна верифікація.

Обмеження:

- залежність від доступності одержувача;
- можливі затримки;
- ризик каскадних тайм-аутів;
- складність масштабування.

Синхронний обмін не повинен створювати циклічні блокування.

## 6.2. Асинхронна взаємодія

Застосовується, коли відправник не повинен чекати завершення операції одержувачем.

```text
MODULE A
   │
   ▼
EVENT STORE
   │
   ▼
DELIVERY CHANNEL
   │
   ▼
MODULE B
   │
   ▼
ACKNOWLEDGEMENT
```

Переваги:

- слабше зв'язування модулів;
- можливість повторного доставлення;
- незалежність життєвих циклів;
- підтримка довготривалих операцій.

Обмеження:

- складніша модель узгодженості;
- можливе повторне доставлення;
- необхідність обробки затримок;
- потреба в контролі порядку.

## 6.3. Правило вибору

```text
IF immediate_result_required:
    USE SYNCHRONOUS

ELSE:
    USE ASYNCHRONOUS
```

Це базове правило.

Остаточний вибір має визначатися контрактом і характеристиками операції.

---

# 7. EVENT DELIVERY GUARANTEES

## 7.1. At-most-once

Повідомлення доставляється не більше одного разу.

Можливий ризик втрати.

## 7.2. At-least-once

Повідомлення доставляється один або більше разів.

Можливі дублікати.

Потребує ідемпотентної обробки.

## 7.3. Exactly-once

У межах розподіленої системи необхідно уникати необґрунтованої обіцянки глобального exactly-once delivery.

Практично реалізується комбінація:

- durable storage;
- unique event identity;
- idempotent consumer;
- atomic local commit;
- deduplication;
- transactional outbox/inbox.

Тому SUBIT використовує формулювання:

**EFFECTIVELY-ONCE PROCESSING WITHIN A DEFINED TRANSACTION BOUNDARY**

Це означає, що повторне доставлення не повинно повторно застосовувати той самий логічний ефект у визначеній області транзакції.

## 7.4. Idempotency

Операція f є ідемпотентною, якщо:

f(f(x)) = f(x)

Для обробки подій:

Apply(Event, State) має бути захищений від повторного застосування тієї самої події.

Для цього використовується:

```text
ProcessedEventRegistry = {
    event_id,
    consumer_id,
    processing_status,
    committed_revision
}
```

Унікальність повинна визначатися щонайменше парою:

(event_id, consumer_id)

Одна подія може бути коректно оброблена різними споживачами.

---

# 8. EVENT STORE AND TRANSACTIONAL OUTBOX

## 8.1. Архітектурне правило

Модулі не повинні безпосередньо обходити SUBIT-DATA для неконтрольованого запису подій.

Операція має проходити через визначену межу фіксації.

## 8.2. Transactional Outbox

Для операцій, які змінюють стан і породжують подію, використовується модель Outbox.

```text
COMMAND
   │
   ▼
VALIDATE
   │
   ▼
LOCAL TRANSACTION
   ├── UPDATE STATE
   └── WRITE OUTBOX EVENT
          │
          ▼
       COMMIT
          │
          ▼
    OUTBOX DISPATCHER
          │
          ▼
      EVENT STORE
```

Ключова властивість:

Зміна локального стану та створення запису Outbox повинні бути атомарними в межах підтримуваної транзакції.

Це запобігає ситуації, коли стан змінився, але відповідна подія не була зафіксована.

## 8.3. Inbox

Одержувач використовує Inbox для контролю вхідних повідомлень.

```text
InboxRecord = (
    message_id,
    consumer_id,
    received_at,
    status,
    result_ref
)
```

Обробка:

1. Отримати повідомлення.
2. Перевірити схему.
3. Перевірити версію контракту.
4. Перевірити idempotency key.
5. Зареєструвати повідомлення в Inbox.
6. Виконати операцію.
7. Зафіксувати результат.
8. Підтвердити доставлення.

Якщо крок 6 завершився помилкою, система повинна мати визначену політику повтору або відхилення.

---

# 9. ORDERING AND CAUSALITY

## 9.1. Час не дорівнює причинності

Для SUBIT принципово важливо розділяти:

- часову послідовність;
- причинну залежність;
- логічний порядок;
- порядок фіксації.

Якщо подія A має часову мітку раніше за B, це саме по собі не доводить, що A спричинила B.

## 9.2. Causal Ordering

Для причинно залежних подій:

A → B

споживач повинен мати можливість встановити, що B залежить від A.

Якщо B отримано раніше за A, споживач може:

- тимчасово відкласти B;
- запросити відсутню залежність;
- обробити B у режимі очікування;
- відхилити повідомлення за правилами контракту.

## 9.3. Event Sequence

Для локального потоку допускається монотонна послідовність:

```text
stream_id
sequence_number
event_id
```

Але sequence_number не є глобальним причинним годинником.

Для розподілених процесів можна використовувати:

- causal parent references;
- Lamport timestamps;
- vector clocks;
- локальні послідовності.

Вибір залежить від вимог конкретного модуля.

## 9.4. Causality Invariant

Якщо B оголошена як DERIVES_FROM(A), посилання на A не повинно бути втрачено під час серіалізації, передавання або зберігання.

---

# 10. CONFLICT RESOLUTION

## 10.1. Типи конфліктів

Визначаються:

- VERSION_CONFLICT;
- STATE_CONFLICT;
- SCHEMA_CONFLICT;
- CAUSALITY_CONFLICT;
- PROVENANCE_CONFLICT;
- CONTEXT_CONFLICT;
- IDENTITY_CONFLICT;
- AUTHORIZATION_CONFLICT.

## 10.2. Загальне правило

Конфлікт не можна вирішувати простим видаленням однієї з альтернатив.

Потрібно зберегти:

- обидва твердження;
- їхні джерела;
- контексти;
- час отримання;
- правила порівняння;
- результат розв'язання.

## 10.3. Conflict Record

```text
Conflict = (
    conflict_id,
    conflict_type,
    subject_ref,
    alternative_a,
    alternative_b,
    context_a,
    context_b,
    provenance_a,
    provenance_b,
    resolution_policy,
    resolution_status
)
```

Можливі статуси:

```text
UNRESOLVED
RESOLVED
PARTIALLY_RESOLVED
REQUIRES_REVIEW
NOT_COMPARABLE
```

`NOT_COMPARABLE` є повноцінним результатом.

Не всі твердження можна коректно порівняти, якщо вони належать до різних контекстів або використовують несумісні визначення.

## 10.4. Belnap/Dunn FOUR

Для логічних конфліктів може застосовуватися окрема чотиризначна логічна модель:

- N = 00 — відсутність обох видів інформації;
- F = 01 — підтримка хибності;
- T = 10 — підтримка істинності;
- B = 11 — підтримка істинності та хибності одночасно.

Це не координати SUBIT-64.

FOUR описує логічний статус твердження, а SUBIT-64 — координатну структуру WHO × WHERE × WHEN.

Протокол повинен зберігати цю відмінність на рівні типів.

---

# 11. RETRY AND FAILURE HANDLING

## 11.1. Класи помилок

```text
TRANSIENT_ERROR
PERMANENT_ERROR
VALIDATION_ERROR
AUTHORIZATION_ERROR
TIMEOUT
RESOURCE_EXHAUSTED
DEPENDENCY_UNAVAILABLE
UNKNOWN_ERROR
```

## 11.2. Retry Policy

Повтор дозволений лише тоді, коли він не створює неконтрольованих побічних ефектів.

```text
RetryPolicy = (
    max_attempts,
    initial_delay,
    max_delay,
    backoff_strategy,
    jitter,
    retryable_errors
)
```

Рекомендована початкова стратегія:

Exponential Backoff with Jitter.

Але точні значення повинні визначатися окремим профілем виконання.

## 11.3. Dead Letter

Повідомлення, яке не вдалося обробити після встановленої кількості спроб, може бути переміщене до Dead Letter Queue.

Це не означає видалення повідомлення.

Воно повинно зберігати:

- початковий Envelope;
- історію спроб;
- причини помилок;
- останній статус;
- посилання на діагностичні дані.

## 11.4. Recovery

Відновлення повинно підтримувати:

1. Повторне доставлення.
2. Повторну валідацію.
3. Відтворення подій.
4. Перевірку цілісності.
5. Повторне застосування ідемпотентних операцій.
6. Переведення повідомлення на ручний розгляд.

Забороняється мовчки відкидати повідомлення, яке містить важливі дані або причинні залежності.

---

# 12. SCHEMA EVOLUTION

## 12.1. Версіонування схем

Кожна схема має власний ідентифікатор:

```text
schema_id
schema_version
schema_owner
compatibility_policy
```

Версія схеми не повинна автоматично дорівнювати версії всього модуля.

## 12.2. Сумісні зміни

Потенційно сумісні:

- додавання необов'язкового поля;
- додавання нового типу повідомлення;
- додавання метаданих;
- уточнення опису без зміни семантики.

## 12.3. Несумісні зміни

Потенційно несумісні:

- зміна типу поля;
- зміна семантики;
- зміна одиниць вимірювання;
- зміна обов'язковості поля;
- зміна правил інтерпретації;
- видалення значущої інформації.

## 12.4. Schema Adapter

Адаптер повинен оголошувати:

```text
SchemaAdapter = (
    adapter_id,
    source_schema,
    target_schema,
    transformation,
    information_loss_policy,
    provenance_policy,
    verification_status
)
```

Якщо адаптер втрачає частину інформації, ця втрата повинна бути явно задекларована.

---

# 13. SECURITY AND TRUST BOUNDARIES

## 13.1. Межі довіри

Не кожен модуль має право надсилати команди кожному іншому модулю.

Для кожної взаємодії визначаються:

- sender identity;
- receiver identity;
- authorization policy;
- data classification;
- allowed operations;
- verification requirements.

## 13.2. Мінімальні вимоги

**SEC-001:** модуль повинен бути ідентифікований.

**SEC-002:** відправник повинен мати право на конкретний тип операції.

**SEC-003:** одержувач повинен перевіряти структуру повідомлення.

**SEC-004:** повідомлення не повинно виконуватися лише на підставі факту отримання.

**SEC-005:** критичні операції повинні мати аудит.

**SEC-006:** секрети й облікові дані не повинні передаватися як звичайний payload.

**SEC-007:** помилки авторизації не повинні автоматично повторюватися без зміни умов.

## 13.3. Trust Is Not Provenance

Provenance описує походження інформації.

Trust описує політику довіри до джерела або операції.

Ці поняття пов'язані, але не тотожні.

Наявність provenance не гарантує істинності.

Наявність довіреного відправника не гарантує правильності кожного його твердження.

---

# 14. MODULE EXCHANGE PROFILES

Протокол визначає кілька профілів обміну.

## PROFILE A — CORE DATA EXCHANGE

Учасники:

- SUBIT-CORE;
- SUBIT-DATA;
- SUBIT-RUNTIME.

Призначення:

- передавання Entity;
- передавання Event;
- збереження Context;
- збереження Provenance;
- контроль ревізій.

Обов'язкові гарантії:

- type safety;
- identity preservation;
- event immutability;
- idempotency.

## PROFILE B — COMPUTATIONAL EXCHANGE

Учасники:

- SUBIT-CPU;
- SUBIT-RUNTIME;
- SUBIT-DATA.

Призначення:

- виконання обчислень;
- передавання результатів;
- фіксація обчислювальних подій;
- контроль побічних ефектів.

Обов'язкові гарантії:

- execution context;
- operation identity;
- resource limits;
- result provenance.

## PROFILE C — AI EXCHANGE

Учасники:

- SUBIT-AI;
- SUBIT-CORE;
- SUBIT-DATA;
- SUBIT-RUNTIME;
- SUBIT-VERIFICATION.

Призначення:

- передавання запитів;
- отримання висновків;
- реєстрація версій моделей;
- фіксація джерел;
- передавання результатів на перевірку.

Ключове правило:

AI_OUTPUT ≠ VERIFIED_FACT

Висновок AI повинен зберігати статус INFERRED або COMPUTED, доки не виконані відповідні критерії підтвердження.

## PROFILE D — VERIFICATION EXCHANGE

Учасники:

- SUBIT-VERIFICATION;
- будь-який модуль, який надає твердження для перевірки.

Призначення:

- передавання claim;
- передавання evidence;
- виконання перевірки;
- реєстрація результату.

Результат повинен містити:

- об'єкт перевірки;
- твердження;
- метод;
- середовище;
- доказ;
- статус;
- обмеження перевірки.

## PROFILE E — AUTONOMOUS APPLICATION EXCHANGE

Застосовується до:

- SUBIT-CHESS;
- SUBIT-WARP;
- SUBIT-BIO;
- SUBIT-LINGUA;
- інших автономних прикладних систем.

Призначення:

- збереження автономності;
- використання спільних контрактів;
- ізоляція внутрішніх алгоритмів;
- контроль міжмодульної сумісності.

Прикладний модуль не повинен бути змушений розкривати всю внутрішню реалізацію для того, щоб надавати коректний контракт.

---

# 15. SUBIT-CHESS REFERENCE FLOW

Цей розділ демонструє застосування протоколу до автономного шахового двигуна.

## 15.1. Послідовність

```text
INPUT POSITION
      │
      ▼
SUBIT-CHESS
      │
      ▼
POSITION VALIDATION
      │
      ▼
LEGAL MOVE GENERATION
      │
      ▼
SUBIT-CPU
      │
      ▼
POSITION ANALYSIS
      │
      ▼
MOVE EVALUATION
      │
      ▼
SEARCH
      │
      ▼
CANDIDATE MOVE
      │
      ▼
VERIFICATION
      │
      ▼
MOVE RESULT
```

## 15.2. Події

Приклад послідовності:

```text
CHESS_POSITION_RECEIVED
CHESS_POSITION_VALIDATED
LEGAL_MOVES_GENERATED
SEARCH_STARTED
POSITION_EVALUATED
CANDIDATE_MOVE_SELECTED
MOVE_VALIDATED
MOVE_COMMITTED
```

Кожна подія має власний event_id.

Причинні зв'язки повинні дозволяти відновити історію аналізу.

## 15.3. Автономність

SUBIT-CHESS не повинен використовувати сторонній шаховий двигун як компонент або джерело рішень.

Не допускається підміна власного пошуку зовнішнім результатом.

Self-play та внутрішньо згенеровані позиції можуть використовуватися для вдосконалення, але кожна зміна евристик або параметрів повинна мати власну версію та незалежну перевірку.

## 15.4. Відокремлення результатів

Необхідно розрізняти:

- LEGALITY — чи дозволений хід правилами;
- EVALUATION — як оцінюється позиція;
- SEARCH_RESULT — що знайшов алгоритм пошуку;
- SELECTION — який хід обрано;
- VERIFICATION — що саме перевірено.

Ці результати не можна зливати в один нечіткий статус «правильний хід».

---

# 16. OBSERVABILITY AND TRACEABILITY

## 16.1. Trace

Trace — сукупність повідомлень, пов'язаних одним correlation_id.

Він дозволяє відновити повний шлях операції.

## 16.2. Span

Span — окремий етап обробки.

```text
Trace
 ├── Span A: Request
 ├── Span B: Validation
 ├── Span C: Computation
 ├── Span D: Persistence
 └── Span E: Response
```

## 16.3. Мінімальні метрики

Для кожного каналу обміну:

- message_count;
- delivery_latency;
- processing_latency;
- retry_count;
- duplicate_count;
- rejection_count;
- timeout_count;
- dead_letter_count;
- schema_validation_failures.

Метрики не повинні замінювати первинні події.

Вони є похідними агрегатами.

## 16.4. Audit Trail

Для критичних операцій повинен існувати відтворюваний журнал:

```text
AuditRecord = (
    audit_id,
    actor,
    operation,
    target,
    context_ref,
    provenance_ref,
    timestamp,
    outcome,
    evidence_ref
)
```

---

# 17. PROTOCOL STATE MACHINE

Кожне повідомлення проходить визначений життєвий цикл.

```text
CREATED
   │
   ▼
VALIDATED
   │
   ▼
QUEUED
   │
   ▼
DELIVERED
   │
   ▼
ACCEPTED
   │
   ▼
PROCESSING
   │
   ├──► COMPLETED
   │
   ├──► REJECTED
   │
   ├──► RETRY_PENDING
   │
   └──► FAILED
```

Додаткові стани:

```text
EXPIRED
QUARANTINED
DEAD_LETTER
CANCELLED
```

## 17.1. Правила переходів

- CREATED → VALIDATED: структура повідомлення перевірена.
- VALIDATED → QUEUED: повідомлення прийняте до каналу.
- QUEUED → DELIVERED: одержувач отримав повідомлення.
- DELIVERED → ACCEPTED: одержувач погодився його обробляти.
- ACCEPTED → PROCESSING: почалася операція.
- PROCESSING → COMPLETED: результат зафіксований.
- PROCESSING → RETRY_PENDING: операція може бути повторена.
- PROCESSING → FAILED: операція остаточно завершилася помилкою.

`DELIVERED` не означає `ACCEPTED`.

`ACCEPTED` не означає `COMPLETED`.

`COMPLETED` не означає `VERIFIED`.

---

# 18. CONFORMANCE LEVELS

Модулі можуть підтримувати протокол на різних рівнях.

## LEVEL 0 — DOCUMENTED

Модуль має задокументовані контракти та структури обміну.

## LEVEL 1 — STRUCTURED

Модуль використовує типізовані повідомлення.

## LEVEL 2 — CONTEXT-AWARE

Модуль зберігає контекст і provenance.

## LEVEL 3 — EVENT-COMPATIBLE

Модуль підтримує подієву модель та ідемпотентну обробку.

## LEVEL 4 — RECOVERABLE

Модуль підтримує повторне доставлення, відновлення та контроль помилок.

## LEVEL 5 — VERIFIABLE

Модуль має формалізовані перевірки відповідності протоколу та відтворювані результати.

Рівень відповідності не є загальною оцінкою якості модуля.

Він описує лише відповідність цьому протоколу.

---

# 19. ACCEPTANCE TESTS

## TEST-PROTO-001 — Message Identity

Повторне передавання не повинно змінювати message_id.

## TEST-PROTO-002 — Context Preservation

Context повинен зберігатися через усі визначені етапи передавання.

## TEST-PROTO-003 — Provenance Preservation

Provenance повинен зберігати посилання на первинне походження.

## TEST-PROTO-004 — Schema Validation

Повідомлення з несумісною схемою не повинно прийматися як коректне.

## TEST-PROTO-005 — Version Compatibility

Несумісна версія повинна бути відхилена або оброблена через задекларований адаптер.

## TEST-PROTO-006 — Idempotency

Повторна обробка того самого повідомлення не повинна створювати повторний логічний ефект.

## TEST-PROTO-007 — Causality

Причинні посилання повинні зберігатися.

## TEST-PROTO-008 — Duplicate Delivery

Дублікати повинні виявлятися за визначеною політикою.

## TEST-PROTO-009 — Failure Recovery

Повідомлення після тимчасової помилки повинно мати можливість контрольованого повторного оброблення.

## TEST-PROTO-010 — Dead Letter Integrity

Переміщення повідомлення до Dead Letter не повинно знищувати його початковий вміст.

## TEST-PROTO-011 — Conflict Preservation

Конфліктні твердження повинні зберігатися як окремі альтернативи.

## TEST-PROTO-012 — FOUR Separation

Чотиризначні логічні значення не повинні трактуватися як координати SUBIT-64.

## TEST-PROTO-013 — Command/Event Separation

Прийнята команда не повинна автоматично трактуватися як завершена подія.

## TEST-PROTO-014 — Verification Separation

COMPLETED не повинно автоматично означати VERIFIED.

## TEST-PROTO-015 — Authorization

Неавторизована команда не повинна виконуватися.

---

# 20. IMPLEMENTATION ROADMAP

Реалізація протоколу повинна відбуватися поступово.

### PHASE 1 — Canonical Schemas

Створити:

- Envelope Schema;
- Message Schema;
- Event Schema;
- Command Schema;
- Context Schema;
- Provenance Schema;
- Causality Schema.

Результат: узгоджена модель даних.

### PHASE 2 — Local Protocol Runtime

Реалізувати:

- schema validation;
- message identity;
- contract lookup;
- version validation;
- local dispatch;
- error handling.

Результат: локальний механізм міжмодульного обміну.

### PHASE 3 — Event Persistence

Реалізувати:

- Event Store;
- Outbox;
- Inbox;
- deduplication;
- replay;
- audit trail.

Результат: надійна подієва інфраструктура.

### PHASE 4 — Context and Provenance

Реалізувати:

- context propagation;
- provenance propagation;
- causal references;
- transformation records;
- context compatibility checks.

Результат: контроль семантичної цілісності.

### PHASE 5 — Verification

Реалізувати:

- conformance tests;
- contract tests;
- schema tests;
- recovery tests;
- trace validation.

Результат: перевірювана відповідність протоколу.

### PHASE 6 — Application Integration

Послідовно під'єднати:

- SUBIT-CHESS;
- SUBIT-WARP;
- SUBIT-BIO;
- SUBIT-LINGUA;
- інші прикладні модулі.

Результат: єдина міжмодульна інфраструктура.

---

# 21. OPEN ARCHITECTURAL QUESTIONS

## Q-001 — Canonical Transport

Чи повинен SUBIT мати власний транспортний протокол?

Попереднє рішення:

Спочатку визначити незалежну від транспорту семантичну модель. Транспортні адаптери можна реалізовувати окремо.

## Q-002 — Serialization

Який формат серіалізації буде основним?

Попереднє рішення:

- YAML — читабельне декларативне представлення;
- JSON — базовий машинозчитуваний формат;
- бінарний формат — можливий наступний етап оптимізації.

Це рекомендація, а не остаточне рішення.

## Q-003 — Distributed Transactions

Чи потрібна глобальна транзакційна модель?

Попереднє рішення:

Не вводити глобальну транзакцію як обов'язкову властивість усієї системи.

Використовувати локальні атомарні транзакції, Outbox/Inbox та явно визначені протоколи узгодження.

## Q-004 — Causality Model

Чи потрібна єдина глобальна модель причинності?

Попереднє рішення:

Визначити канонічний формат причинних посилань, але дозволити різні моделі порядку в різних підсистемах.

## Q-005 — Context Compatibility

Як визначати сумісність контекстів?

Попереднє рішення:

Ввести окрему процедуру Context Compatibility Assessment.

Не вважати контексти сумісними лише тому, що вони мають однакову структуру полів.

## Q-006 — Semantic Validation

Чи повинні всі модулі перевіряти семантичну коректність отриманих повідомлень?

Попереднє рішення:

Так, але в межах власної компетенції.

SUBIT-CORE перевіряє структурні інваріанти.

SUBIT-LANG — типи та схеми.

SUBIT-RUNTIME — правила виконання.

SUBIT-VERIFICATION — визначені критерії доказовості.

Прикладний модуль — власну предметну семантику.

---

# 22. FINAL ARCHITECTURAL PRINCIPLE

SUBIT-64 CROSS-MODULE CONTRACT PROTOCOL формалізує спосіб, у який різні модулі можуть взаємодіяти, не втрачаючи власної ідентичності.

Модулі можуть мати різні:

- онтології;
- моделі даних;
- обчислювальні механізми;
- методи;
- часові масштаби;
- критерії перевірки;
- контексти інтерпретації.

Але їхня взаємодія повинна бути структурно визначеною.

Тому міжмодульний протокол не повинен примушувати всі модулі до однакової внутрішньої організації.

Він повинен визначати, як відмінності можуть передаватися, зіставлятися та узгоджуватися.

Формула:

SUBIT EXCHANGE = IDENTITY + MESSAGE + CONTEXT + PROVENANCE + CAUSALITY + CONTRACT

Інформація, позбавлена контексту, може втратити значення.

Інформація, позбавлена provenance, може втратити перевірюваність.

Інформація, позбавлена причинних зв'язків, може втратити історію свого виникнення.

Тому:

**DO NOT COLLAPSE — CONTEXTUALIZE.**

**END OF SPECIFICATION v1.0**