# SUBIT-WARP v0.4
## W45 — Lean 4 Formalization Blueprint

**Версія:** W45 v0.1  
**Статус:** FORMALIZATION ARCHITECTURE DRAFT  
**Проєкт:** SUBIT-WARP v0.4  
**Базовий принцип:** DO NOT COLLAPSE — CONTEXTUALIZE  
**Попередні документи:** W39, W39.1, W40, W41, W42, W43, W44  
**Цільова система:** Lean 4  
**Mathlib:** використання передбачається, але конкретну версію ще не зафіксовано  
**Kernel verification:** NOT PERFORMED  
**GitHub:** змін не внесено

---

# 1. Мета

W45 визначає архітектуру формальної верифікації SUBIT-WARP v0.4 у Lean 4.

Завдання — перевести математичну модель W39–W44 у формальну систему, в якій:

1. типи об'єктів визначені однозначно;
2. некоректні коди відокремлені від допустимих;
3. структурне кодування та декодування мають явні домени;
4. нескінченні гілки визначені через формальні предикати;
5. boundary map має доведені властивості;
6. метричні твердження використовують узгоджені типи та метрики;
7. спектральні результати відокремлені від структурних;
8. кожна теорема має простежувану залежність від означень;
9. аксіоми, припущення та незавершені докази явно обліковуються.

W45 не є реалізацією та не є звітом про Lean-компіляцію. Це архітектура майбутньої реалізації.

---

# 2. Принципи формалізації

## 2.1. Типова безпека

Формалізація повинна розрізняти:

- довільний код;
- локально допустимий код;
- rooted-код;
- повний код;
- код із нескінченним продовженням;
- код із непорожньою межею.

Не слід використовувати один загальний тип для всіх цих категорій, якщо це приховує їхні різні інваріанти.

## 2.2. Не ототожнювати структуру та її кодування

Структурне дерево і його адресний код — різні типи.

Їхня еквівалентність має бути результатом доведення, а не неявного припущення реалізації.

## 2.3. Не ототожнювати скінченне та нескінченне

Скінченні апроксимації можуть бути корисними для обчислень, але не замінюють нескінченних об'єктів.

Зокрема:

- скінченна глибина не доводить нескінченного продовження;
- скінченний тест не доводить коіндуктивної рівності;
- гранична множина не може бути визначена лише через скінченну апроксимацію без окремої теореми.

## 2.4. Не приховувати припущення

Заборонено маскувати невиконані доказові зобов'язання через:

- `sorry`;
- необґрунтовані `axiom`;
- `admit`;
- неперевірені зовнішні твердження;
- неявні припущення про скінченність або повноту.

Проміжні незавершені теореми дозволені лише в окремій робочій гілці формалізації та не можуть бути позначені як verified.

---

# 3. Архітектура модулів

Пропонується така структура:

```text
SubitWarp/
├── Basic/
│   ├── Alphabet.lean
│   ├── Address.lean
│   └── State.lean
│
├── Tree/
│   ├── PartialTree.lean
│   ├── RootedTree.lean
│   ├── FullTree.lean
│   └── TreeEquiv.lean
│
├── Code/
│   ├── RawCode.lean
│   ├── Closure.lean
│   ├── PartialCode.lean
│   └── FullCode.lean
│
├── Encoding/
│   ├── Encode.lean
│   ├── Decode.lean
│   ├── Bisimulation.lean
│   └── RoundTrip.lean
│
├── Infinite/
│   ├── InfiniteBranch.lean
│   ├── Konig.lean
│   └── OmegaTree.lean
│
├── Metric/
│   ├── CodeMetric.lean
│   ├── BoundaryMetric.lean
│   └── Hausdorff.lean
│
├── Boundary/
│   ├── Boundary.lean
│   ├── Compactness.lean
│   └── Stability.lean
│
├── Spectral/
│   ├── CylinderSpace.lean
│   ├── HaarMeasure.lean
│   ├── Wavelets.lean
│   ├── DecreasingKernel.lean
│   ├── IncreasingKernel.lean
│   └── Approximation.lean
│
├── Regression/
│   ├── W20.lean
│   ├── W39_W44.lean
│   └── EdgeCases.lean
│
└── Verification/
    ├── AxiomAudit.lean
    ├── TheoremInventory.lean
    └── ReleaseChecks.lean
```

Це логічна архітектура. Остаточна структура файлів залежатиме від конкретної версії Lean 4 та Mathlib.

---

# 4. Базові типи

## 4.1. Алфавіт дочірніх позицій

Для скінченного branching factor b≥2:

```lean
def Branch (b : ℕ) (hb : 2 ≤ b) := Fin b
```

Використання `Fin b` забезпечує типобезпечний індекс дочірнього слота.

Потрібно уникати неформального використання натуральних чисел із подальшим припущенням, що індекс належить допустимому діапазону.

## 4.2. Адреси

```lean
abbrev Address (b : ℕ) := List (Fin b)
```

Порожній список є кореневою адресою.

```lean
def rootAddress : Address b := []
```

Конкатенація дочірнього індексу:

```lean
def childAddress (u : Address b) (i : Fin b) : Address b :=
  u ++ [i]
```

Необхідні леми:

- довжина адреси після додавання дочірнього індексу;
- збереження префікса;
- асоціативність конкатенації;
- відмінність адрес різних дочірніх позицій.

## 4.3. Кодові стани

```lean
inductive CodeState (A : Type)
  | absent
  | internal
  | leaf (value : A)
```

Цей тип навмисно не містить UNKNOWN.

UNKNOWN не можна додавати без окремого визначення його семантики.

Якщо він буде введений у майбутній версії, це має бути окреме розширення кодового алфавіту, а не перевизначення `absent`.

---

# 5. Тип структурного дерева

## 5.1. Основний коіндуктивний тип

Концептуальна модель:

```lean
inductive PartialTree (A : Type) (b : ℕ)
  | none
  | leaf (value : A)
  | node (children : Fin b → PartialTree A b)
```

Це означення є ілюстрацією структурного типу. Воно не є автоматично коіндуктивною реалізацією нескінченного дерева.

Для нескінченних дерев потрібен окремий тип або представлення через функції на адресах із доведеними closure-інваріантами.

У Lean 4 можна розглядати два підходи:

**Підхід A — Coinductive structure.**

Використати коіндуктивне представлення, якщо його реалізація сумісна з вимогами Lean щодо guarded corecursion.

**Підхід B — Address-indexed representation.**

Представляти дерево функцією:

`Address b → CodeState A`

з предикатами локальної допустимості.

Для SUBIT-WARP рекомендовано починати з підходу B, оскільки він безпосередньо узгоджується з C_Partial та d_code.

Коіндуктивну структурну модель можна додати як окрему альтернативну репрезентацію.

---

# 6. RawCode та допустимі підтипи

## 6.1. RawCode

```lean
abbrev RawCode (A : Type) (b : ℕ) :=
  Address b → CodeState A
```

Це тип усіх функцій, незалежно від структурної коректності.

## 6.2. ABSENT closure

Концептуальний предикат:

```lean
def AbsentClosed (t : RawCode A b) : Prop :=
  ∀ u v,
    IsPrefix u v →
    t u = .absent →
    t v = .absent
```

`IsPrefix` має бути окремо визначений і перевірений.

## 6.3. LEAF closure

```lean
def LeafClosed (t : RawCode A b) : Prop :=
  ∀ u v a,
    IsStrictPrefix u v →
    t u = .leaf a →
    t v = .absent
```

## 6.4. Rootedness

```lean
def Rooted (t : RawCode A b) : Prop :=
  t rootAddress ≠ .absent
```

## 6.5. PartialCode

```lean
def PartialCode (A : Type) (b : ℕ) :=
  { t : RawCode A b //
      AbsentClosed t ∧
      LeafClosed t ∧
      Rooted t }
```

## 6.6. FullCode

```lean
def FullCode (A : Type) (b : ℕ) :=
  { t : PartialCode A b //
      ∀ u,
        t.1 u = .internal →
        ∀ i : Fin b,
          t.1 (childAddress u i) ≠ .absent }
```

Уточнення: типи в цьому розділі є blueprint-поданням. Перед використанням необхідно перевірити, що всі залежні параметри, coercions і proof fields узгоджені з реальною реалізацією Lean.

---

# 7. Encoding та Decoding

## 7.1. Encoding

```lean
def encode
  (x : RootedTree A b) :
  PartialCode A b
```

Функція повинна повертати не RawCode, а доведено допустимий PartialCode.

Це дозволяє отримати closure-властивості без повторного доведення при кожному використанні результату.

## 7.2. Decoding

```lean
def decode
  (t : PartialCode A b) :
  RootedTree A b
```

Декодування приймає лише допустимий код.

Заборонено робити декодування довільного RawCode без явної перевірки інваріантів.

## 7.3. Round-trip theorem 1

```lean
theorem decode_encode
  (x : RootedTree A b) :
  decode (encode x) = x
```

Це структурна теорема W43-T1.

## 7.4. Round-trip theorem 2

```lean
theorem encode_decode
  (t : PartialCode A b) :
  encode (decode t) = t
```

Це структурна теорема W43-T2.

Обидва твердження мають бути доведені без додаткових аксіом.

## 7.5. Рівність функціональних кодів

Для другого round-trip необхідно використати функціональну екстенсіональність або еквівалентний доказ рівності функцій.

Однак сама функціональна екстенсіональність не замінює структурного доказу: треба показати рівність станів на кожній адресі.

---

# 8. Нескінченні гілки

## 8.1. Prefix relation

Потрібно формально визначити:

```lean
def IsPrefix (u v : Address b) : Prop := ...
```

та:

```lean
def IsStrictPrefix (u v : Address b) : Prop := ...
```

## 8.2. Infinite address

Нескінченна адреса може бути представлена як:

```lean
abbrev InfiniteAddress (b : ℕ) :=
  ℕ → Fin b
```

Префікс довжини n:

```lean
def prefix (ξ : InfiniteAddress b) (n : ℕ) :
  Address b := ...
```

## 8.3. InfiniteBranch

```lean
def InfiniteBranch (t : PartialCode A b)
  (ξ : InfiniteAddress b) : Prop :=
  ∀ n, t.1 (prefix ξ n) = .internal
```

## 8.4. Infinite continuation

```lean
def HasInfiniteContinuation
  (t : PartialCode A b)
  (u : Address b) : Prop :=
  t.1 u = .internal ∧
  ∃ ξ : InfiniteAddress b,
    IsPrefix u (prefix ξ (length u)) ∧
    ∀ n, length u ≤ n →
      t.1 (prefix ξ n) = .internal
```

Точне формальне означення потребує узгодження представлення адреси ξ із префіксом u.

Не можна використовувати лише умову нескінченного продовження від кореня, якщо теорема стосується довільного INTERNAL-вузла.

## 8.5. Tω_P

```lean
def OmegaPartial
  (t : PartialCode A b) : Prop :=
  ∀ u,
    t.1 u = .internal →
    HasInfiniteContinuation t u
```

## 8.6. Tω_P⁺

```lean
def OmegaPartialPlus
  (t : PartialCode A b) : Prop :=
  OmegaPartial t ∧
  t.1 rootAddress = .internal
```

Важлива властивість:

Rooted LEAF-код може задовольняти OmegaPartial вакуумно, оскільки він не має INTERNAL-вузлів.

Але він не задовольняє OmegaPartialPlus.

Це має бути відображено в regression tests.

---

# 9. Boundary map

## 9.1. Boundary

```lean
def Boundary
  (t : PartialCode A b) :
  Set (InfiniteAddress b) :=
  { ξ | InfiniteBranch t ξ }
```

Для t ∈ Tω_P⁺ потрібно довести:

1. Boundary t непорожня;
2. Boundary t замкнена;
3. Boundary t компактна в добутковій топології.

## 9.2. Nonempty boundary

```lean
theorem boundary_nonempty
  (t : PartialCode A b)
  (ht : OmegaPartialPlus t) :
  (Boundary t).Nonempty
```

Доказ має використовувати нескінченне продовження кореня.

## 9.3. Closed boundary

```lean
theorem boundary_closed
  (t : PartialCode A b) :
  IsClosed (Boundary t)
```

Доказ спирається на те, що порушення умови нескінченної INTERNAL-гілки виявляється на скінченному префіксі.

## 9.4. Compact boundary

Компактність залежить від компактності Σ_b.

Потрібно окремо формалізувати:

- топологію добутку;
- компактність скінченного дискретного алфавіту;
- компактність простору нескінченних послідовностей;
- замкненість Boundary.

Не можна посилатися на компактність Σ_b без зафіксованої топологічної структури.

---

# 10. Кодова ультраметрика

## 10.1. Перша відмінна глибина

Потрібно визначити r_code(t,s) як найменшу глибину, на якій існує адреса з різними станами.

Оскільки множина адрес на кожному рівні скінченна, мінімум за непорожньої множини глибин існує.

Для однакових кодів перша відмінність відсутня.

## 10.2. Метричне означення

```lean
def codeDistance (t s : RawCode A b) : ℝ := ...
```

Формула:

d_code(t,s)=2^(−r_code(t,s)).

У реалізації необхідно обрати узгоджене представлення нескінченної глибини та нульової відстані.

Альтернативний підхід — визначити відстань через найбільшу спільну глибину узгодженості. Це може спростити формальне доведення ультраметричної нерівності.

## 10.3. Proof obligations

- невід'ємність;
- симетричність;
- тотожність нерозрізнюваних кодів;
- ультраметрична нерівність.

Після цього метрика обмежується на PartialCode, FullCode, Tω_P та Tω_P⁺.

---

# 11. Boundary stability

W39.1 та W41 встановлюють:

d_H,Σ(∂f,∂g) ≤ 2d_code(f,g).

У Lean це потребує:

1. формального Hausdorff distance;
2. компактності меж;
3. непорожності меж;
4. доказу відповідності префіксів;
5. симетричного аргументу для обох напрямків.

Критично: не можна доводити цю оцінку лише для скінченних апроксимацій, а потім без обґрунтування переносити її на нескінченні дерева.

Окремо потрібно перевірити крайовий випадок першої відмінності на глибині m=1 та доведення неможливості m=0 для двох дерев із Tω_P⁺.

Оптимальність константи 2, заявлена у W41, повинна отримати окремий формальний контрприклад або бути знижена до статусу OPEN.

---

# 12. Спектральний модуль

Спектральну частину потрібно реалізовувати після завершення структурних модулів.

Її залежності:

- Σ_b;
- циліндрична топологія;
- рівномірна міра μ_b;
- L²-простір;
- ортогональні проєкції P_n;
- wavelet-підпростори W_j.

## 12.1. Циліндричні функції

Для адреси u довжини n:

[u] = {ξ ∈ Σ_b : ξ|n=u}.

Рівномірна міра:

μ_b([u])=b^(−n).

## 12.2. Wavelet decomposition

H = H₀ ⊕ ⨁_{j≥1} W_j.

dim(W_j)=(b−1)b^(j−1).

Ці твердження мають бути доведені на основі конкретної реалізації L²(Σ_b,μ_b).

## 12.3. Спадне ядро

K_q(ξ,η)=q^{ℓ(ξ,η)}.

Необхідно довести:

- інтегровність ядра;
- симетричність оператора;
- формули власних значень;
- кратності;
- trace-class властивість;
- крайові випадки q=0 та q=1.

## 12.4. Зростаюче ядро

K_t(ξ,η)=t^{ℓ(ξ,η)}.

Необхідно окремо довести:

- boundedness для 1<t<b;
- compactness;
- Hilbert–Schmidt поріг t²<b;
- відсутність trace-class для t>1;
- необмеженість інтегральної форми для t≥b.

Не можна переносити спектральні результати між спадним і зростаючим ядрами без окремого доведення.

## 12.5. Спектральні залежності

W42 формули мають статус текстового математичного результату.

Їхня відповідність історичному W30 залишається відкритою до прямого звірення.

---

# 13. Regression та тестова архітектура

Тести поділяються на чотири класи.

**Class A — Type-level checks**

- коректність типів;
- параметризація через b;
- rootedness;
- відокремлення UNKNOWN.

**Class B — Finite structural checks**

- Leaf;
- Node;
- ABSENT;
- branching;
- closure;
- round-trip на скінченних прикладах.

**Class C — Infinite structural checks**

- нескінченна гілка;
- infinite continuation;
- Tω_P;
- boundary preservation;
- коіндуктивна рівність.

**Class D — Analytical checks**

- метрика;
- компактність;
- оператори;
- спектр;
- trace-class;
- Hilbert–Schmidt.

Скінченні тести не замінюють математичних доказів класів C і D.

---

# 14. Виправлення, що переходить із W44

W44-R020 потребує точнішого формулювання.

Попереднє формулювання:

«Скінченне rooted tree без нескінченного INTERNAL-продовження не повинно належати Tω_P».

Воно надто широке.

Коректне формулювання:

Якщо скінченне rooted tree має принаймні один INTERNAL-вузол, то воно не належить Tω_P.

Якщо корінь є LEAF і INTERNAL-вузлів немає, умова OmegaPartial виконується вакуумно.

Отже:

- Rooted LEAF tree ∈ Tω_P;
- Rooted LEAF tree ∉ Tω_P⁺;
- скінченне rooted tree з INTERNAL-вузлом ∉ Tω_P.

Це уточнення має бути перенесене до W44.1 або до наступної редакції регресійної матриці.

---

# 15. Аксіоматична політика

Формалізація повинна мати окремий аудит аксіом.

Дозволені лише:

- стандартні аксіоми Lean;
- явно задокументовані аксіоми Mathlib;
- математичні припущення, що є частиною теореми.

Неприпустимо використовувати аксіоми для обходу доказів:

- round-trip;
- compactness;
- boundary nonemptiness;
- spectral formulas;
- operator boundedness.

Для кожної критичної теореми потрібно документувати:

1. використані аксіоми;
2. залежності від Mathlib;
3. зовнішні припущення;
4. статус доказу.

Рекомендований інструментальний контроль — аудит `#print axioms` для ключових теорем після завершення формалізації.

---

# 16. Етапи реалізації

## F0 — Environment freeze

Зафіксувати:

- версію Lean 4;
- версію Mathlib;
- toolchain;
- залежності;
- спосіб відтворення збірки.

Результат: відтворюване середовище.

## F1 — Basic types

Реалізувати:

- Branch;
- Address;
- CodeState;
- RawCode.

Результат: базові типи компілюються.

## F2 — Structural constraints

Реалізувати:

- AbsentClosed;
- LeafClosed;
- Rooted;
- PartialCode;
- FullCode.

Результат: коректні підтипи кодів.

## F3 — Encoding/Decoding

Реалізувати:

- encode;
- decode;
- round-trip теореми.

Результат: структурна бієкція W43.

## F4 — Infinite continuation

Реалізувати:

- InfiniteAddress;
- InfiniteBranch;
- HasInfiniteContinuation;
- OmegaPartial;
- OmegaPartialPlus.

Результат: формальні Tω_P та Tω_P⁺.

## F5 — Boundary

Реалізувати:

- Boundary;
- nonempty;
- closed;
- compact;
- boundary preservation.

Результат: формальний T-007.

## F6 — Metric

Реалізувати:

- d_code;
- ultrametric;
- Hausdorff metric;
- boundary stability.

Результат: метричні теореми W39.1/W41.

## F7 — Spectral

Реалізувати:

- μ_b;
- H;
- H_n;
- W_j;
- оператори;
- спектральні теореми.

Результат: формалізація W42.

## F8 — Regression

Відновити W20, додати W44 тести, виконати регресійний аудит.

Результат: відтворювана регресійна матриця.

## F9 — Release verification

Виконати:

- повну збірку;
- аудит аксіом;
- перевірку всіх залежностей;
- відтворення тестів;
- аудит джерел.

Результат: доказова база для рішення про стабілізацію.

---

# 17. Критерії формальної готовності

Модуль не може бути позначений як завершений лише тому, що його файл компілюється.

Для кожного модуля потрібні:

1. точні типи;
2. повні означення;
3. теореми;
4. докази;
5. тестові приклади;
6. аудит аксіом;
7. відсутність неприпустимих `sorry`;
8. відтворювана збірка.

Статуси:

- **SPECIFIED** — означення зафіксовані;
- **IMPLEMENTED** — код написано;
- **COMPILED** — модуль компілюється;
- **KERNEL-VERIFIED** — твердження перевірені ядром Lean;
- **REGRESSION-PASSED** — регресійні тести пройшли;
- **RELEASE-READY** — виконані всі критерії релізу.

Ці статуси не взаємозамінні.

---

# 18. Реєстр формалізаційних зобов'язань

| ID | Компонент | Залежність | Статус |
|---|---|---|---|
| W45-F001 | Branch type | Basic | SPECIFIED |
| W45-F002 | Address type | Basic | SPECIFIED |
| W45-F003 | CodeState | Basic | SPECIFIED |
| W45-F004 | RawCode | Code | SPECIFIED |
| W45-F005 | ABSENT closure | Code | SPECIFIED |
| W45-F006 | LEAF closure | Code | SPECIFIED |
| W45-F007 | Rooted code | Code | SPECIFIED |
| W45-F008 | Full code | Code | SPECIFIED |
| W45-F009 | Structural tree | Tree | BLUEPRINT |
| W45-F010 | Encoding | Encoding | BLUEPRINT |
| W45-F011 | Decoding | Encoding | BLUEPRINT |
| W45-F012 | Round-trip 1 | Encoding | PENDING |
| W45-F013 | Round-trip 2 | Encoding | PENDING |
| W45-F014 | Infinite branch | Infinite | BLUEPRINT |
| W45-F015 | Tω_P | Infinite | PENDING |
| W45-F016 | Tω_P⁺ | Infinite | PENDING |
| W45-F017 | Boundary nonempty | Boundary | PENDING |
| W45-F018 | Boundary closed | Boundary | PENDING |
| W45-F019 | Boundary compact | Boundary | PENDING |
| W45-F020 | d_code | Metric | BLUEPRINT |
| W45-F021 | Ultrametric proof | Metric | PENDING |
| W45-F022 | Hausdorff estimate | Metric | PENDING |
| W45-F023 | Spectral decomposition | Spectral | PENDING |
| W45-F024 | Decreasing kernel | Spectral | PENDING |
| W45-F025 | Increasing kernel | Spectral | PENDING |
| W45-F026 | W20 regression | Regression | SOURCE-CHECK |

---

# 19. Підсумковий висновок

W45 визначає шлях від математичної специфікації SUBIT-WARP до формальної верифікації в Lean 4.

Основне архітектурне рішення — розділити:

- базові типи;
- структурні дерева;
- адресні коди;
- допустимі підтипи;
- кодування та декодування;
- нескінченні гілки;
- граничну структуру;
- метрику;
- спектральну теорію;
- регресійні перевірки.

Таке розділення зменшує ризик того, що одна властивість буде неявно використана як інша.

Особливо важливо, що структурна бієкція W43, boundary map W41 та спектральна модель W42 мають незалежні доказові зобов'язання. Жоден із цих результатів не можна вважати автоматичним наслідком іншого.

**Підсумковий статус W45:**

- Lean architecture: SPECIFIED.
- Basic type design: SPECIFIED.
- Structural encoding/decoding: BLUEPRINT.
- Round-trip proofs: PENDING.
- Infinite-tree formalization: BLUEPRINT.
- Boundary formalization: PENDING.
- Metric formalization: PENDING.
- Spectral formalization: PENDING.
- W20 source compatibility: PENDING.
- Lean implementation: NOT PERFORMED.
- Kernel verification: NOT PERFORMED.
- GitHub integration: NOT PERFORMED.
- SUBIT-WARP v0.4: DRAFT / NOT STABLE.

**Головний принцип W45:** формальна верифікація повинна підтверджувати математичну структуру SUBIT-WARP, а не лише компілювати її програмне представлення. Якщо певна властивість не доведена, вона повинна залишатися явно відкритою.