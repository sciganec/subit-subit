# SUBIT-WARP v0.3 — незалежний аудит W10: Computational and Formal Verification

W10 — це перехід від математично сформульованої теорії до системи перевірюваних обчислювальних і формальних тверджень.

Після аудиту W0–W9 маємо достатньо результатів, щоб побудувати повноцінний verification framework. Але важливо не змішувати три різні статуси:

* **Mathematically proved** — твердження доведене математично.
* **Numerically verified** — твердження перевірене обчисленнями для конкретних параметрів і рівнів.
* **Formally verified** — твердження доведене у формальній системі, наприклад Lean.

Ці статуси не взаємозамінні.

## 1. Загальний висновок аудиту W10

Архітектура WARP має хорошу основу для обчислювальної верифікації:

1. Відомі точні формули матриці M⁽ⁿ⁾.
2. Відомий повний спектр скінченнорівневої матриці.
3. Відомі кратності власних значень.
4. Відомі точні формули операторної та спектральної похибок.
5. Відомі залежності між параметрами αᵥ, α𝑤, q, β та Dᵥ.

Це дозволяє побудувати тести, які перевіряють не лише правильність окремих обчислень, а й узгодженість усієї математичної архітектури.

Однак є важливе застереження: **чисельна перевірка скінченних матриць не доводить теореми про нескінченновимірний оператор**. Вона перевіряє їхні скінченні наслідки.

---

# 2. Архітектура Verification Framework

Пропоную розділити W10 на п'ять незалежних шарів.

| Шар | Назва                   | Що перевіряє                            |
| --- | ----------------------- | --------------------------------------- |
| V1  | Structural Verification | Дерево, адреси, циліндри                |
| V2  | Metric Verification     | Ультраметрика, геометричні параметри    |
| V3  | Operator Verification   | Ядра, інтеграли, операторні властивості |
| V4  | Spectral Verification   | Власні значення, кратності, похибки     |
| V5  | Formal Verification     | Формальні математичні докази            |

Це розділення принципове.

Наприклад, тест V4 може підтвердити, що матриця 27 × 27 має очікуваний спектр із заданою чисельною точністю. Але він не доводить компактність оператора T_q на нескінченному просторі.

Аналогічно, формальний доказ компактності не підтверджує, що програмна реалізація матриці правильно обчислює спільні префікси.

Тому кожен шар повинен мати власні критерії прийняття.

---

# 3. V1 — Structural Verification

Перший шар перевіряє дискретну структуру.

Нехай:

B = {1, 2, 3},

Pos = B⁽<ω⁾,

Σ = Bᴺ.

Циліндр адреси σ:

Cσ = {ξ ∈ Σ : ξ|ₙ = σ},

де |σ| = n.

Для кожного n:

|Bⁿ| = 3ⁿ.

Міра циліндра:

μ(Cσ) = 3⁻ⁿ.

### Обов'язкові тести

| ID      | Перевірка                         | Очікуваний результат |   |   |   |   |
| ------- | --------------------------------- | -------------------- | - | - | - | - |
| STR-001 | Кількість адрес рівня n           | 3ⁿ                   |   |   |   |   |
| STR-002 | Кількість дочірніх адрес          | 3 на кожну адресу    |   |   |   |   |
| STR-003 | Міра циліндра                     | 3⁻ⁿ                  |   |   |   |   |
| STR-004 | Сума мір рівня                    | 1                    |   |   |   |   |
| STR-005 | Вкладення циліндрів               | Cσ = Cσ1 ∪ Cσ2 ∪ Cσ3 |   |   |   |   |
| STR-006 | Неперетинність дочірніх циліндрів | Попарно неперетинні  |   |   |   |   |
| STR-007 | Спільний префікс                  | 0 ≤ ℓ(σ,τ) ≤ min(    | σ | , | τ | ) |

Особливо важливий STR-005:

μ(Cσ) = μ(Cσ1) + μ(Cσ2) + μ(Cσ3).

Цей тест контролює узгодженість ієрархічної міри.

### Критерій прийняття

Усі структурні властивості повинні виконуватися точно, без чисельних допусків.

Для скінченних адрес це звичайні комбінаторні твердження, які можна перевірити повністю.

---

# 4. V2 — Metric Verification

Тут перевіряються дві метрики:

d_S(ξ,η) = 2⁻ˡ

і

dᵥ(ξ,η) = exp(−αᵥℓ).

Перший важливий тест:

**dᵥ(ξ,η) = d_S(ξ,η)^(αᵥ/ln 2).**

Для довільних трьох точок повинна виконуватися ультраметрична нерівність:

dᵥ(ξ,ζ) ≤ max(dᵥ(ξ,η), dᵥ(η,ζ)).

### Тестова матриця

| ID      | Перевірка                 | Очікуваний результат |
| ------- | ------------------------- | -------------------- |
| MET-001 | Симетричність             | d(ξ,η) = d(η,ξ)      |
| MET-002 | Невід'ємність             | d ≥ 0                |
| MET-003 | Розділення точок          | d = 0 ⇔ ξ = η        |
| MET-004 | Ультраметрична нерівність | Виконується          |
| MET-005 | Еквівалентність формул dᵥ | Чисельно узгоджені   |
| MET-006 | Параметр αᵥ > 0           | Обов'язкова умова    |
| MET-007 | Розмірність               | Dᵥ = ln 3/αᵥ         |

### Важлива межа чисельної перевірки

MET-004 можна перевіряти на великій кількості випадково згенерованих скінченних префіксів.

Але випадкове тестування не доводить ультраметричність для всіх точок Σ.

Для формального доказу потрібно використати властивість спільного префікса:

ℓ(ξ,ζ) ≥ min{ℓ(ξ,η), ℓ(η,ζ)}.

Це вже математичний доказ, а не статистичне спостереження.

---

# 5. V3 — Operator Verification

Цей шар перевіряє ядро:

K_q(ξ,η) = q^ℓ(ξ,η), якщо ξ ≠ η,

K_q(ξ,ξ) = 0.

За умов:

0 < q < 1.

## 5.1. Інтегральна константа

Точна формула:

c_q = 2/(3 − q).

Тест:

∫Σ K_q(ξ,η)dμ(η) = c_q.

Важливо перевіряти її для різних фіксованих ξ.

Через симетрію дерева результат не повинен залежати від вибору ξ.

## 5.2. Симетричність ядра

K_q(ξ,η) = K_q(η,ξ).

Звідси випливає самоспряженість T_q.

## 5.3. Компактність

Оскільки:

|K_q(ξ,η)| ≤ 1,

а μ є ймовірнісною мірою:

∫Σ×Σ |K_q|² d(μ × μ) ≤ 1.

Тому:

K_q ∈ L²(Σ × Σ, μ × μ).

Отже, T_q є оператором Гільберта — Шмідта і, відповідно, компактним.

Це доведений математичний результат, який не потребує чисельної перевірки.

### Критерії

| ID      | Перевірка                     | Статус |
| ------- | ----------------------------- | ------ |
| OPR-001 | Симетричність ядра            | PROVED |
| OPR-002 | Обмеженість ядра              | PROVED |
| OPR-003 | Квадратична інтегровність     | PROVED |
| OPR-004 | Компактність T_q              | PROVED |
| OPR-005 | Інтеграл c_q                  | PROVED |
| OPR-006 | Дія на сталих функціях        | PROVED |
| OPR-007 | Додатна напіввизначеність T_q | FALSE  |

Останній пункт особливо важливий.

Не можна додавати тест, який очікує, що T_q буде додатно напіввизначеним.

Його власні значення λⱼ(q) від'ємні для всіх j ≥ 1.

Натомість:

L_q = T_q − c_qI

є від'ємно напіввизначеним.

---

# 6. V4 — Spectral Verification

Це центральний обчислювальний шар WARP.

## 6.1. Точні спектральні формули

Для j ≥ 1:

λⱼ(q) = −(1 − q)qʲ⁻¹ / [3ʲ⁻¹(3 − q)].

Для нормалізованого оператора:

τⱼ(q) = λⱼ(q) − c_q.

Кратність:

mⱼ = 2·3ʲ⁻¹.

Для скінченного рівня n:

Spec(T_q⁽ⁿ⁾) = {c_q} ∪ {λ₁,…,λₙ}.

Spec(L_q⁽ⁿ⁾) = {0} ∪ {τ₁,…,τₙ}.

### 6.2. Обов'язкові спектральні тести

| ID      | Перевірка                       | Очікуваний результат |
| ------- | ------------------------------- | -------------------- |
| SPC-001 | Симетричність M⁽ⁿ⁾              | True                 |
| SPC-002 | Власне значення сталого вектора | c_q                  |
| SPC-003 | Власне значення λ₁              | Точна формула        |
| SPC-004 | Власне значення λⱼ              | Точна формула        |
| SPC-005 | Кратність λⱼ                    | 2·3ʲ⁻¹               |
| SPC-006 | Сума кратностей                 | 3ⁿ                   |
| SPC-007 | Спектр L_q⁽ⁿ⁾                   | Очікувана множина    |
| SPC-008 | Від'ємна напіввизначеність L_q  | Виконується          |
| SPC-009 | Збіжність λⱼ до нуля            | Виконується          |
| SPC-010 | Збіжність τⱼ до −c_q            | Виконується          |

## 6.3. Точна операторна похибка

Перевіряється:

‖T_q − PₙT_qPₙ‖ = |λₙ₊₁(q)|.

Тобто:

Eₙ = (1 − q)qⁿ/[3ⁿ(3 − q)].

Тест повинен перевіряти не просто монотонне зменшення Eₙ, а саме точну формулу.

## 6.4. Спектральна похибка

Перевіряється:

d_H(Spec(L_q⁽ⁿ⁾), Spec(L_q)) = |λₙ(q)|.

Тобто:

Sₙ = (1 − q)qⁿ⁻¹/[3ⁿ⁻¹(3 − q)].

Важливо не плутати Eₙ і Sₙ:

Eₙ = |λₙ₊₁|,

Sₙ = |λₙ|.

Отже:

Sₙ = 3Eₙ/q.

Це співвідношення також варто включити до тестів.

---

# 7. Рекурсивна структура матриці — важливе архітектурне покращення

Під час аудиту W10 виявляється можливість суттєво оптимізувати реалізацію.

Пряме формування матриці M⁽ⁿ⁾ потребує зберігання 9ⁿ елементів.

Але матриця має рекурсивну структуру.

Позначимо:

N = 3ⁿ⁻¹,

J_N — матрицю N × N, усі елементи якої дорівнюють 1.

Тоді:

**M⁽ⁿ⁾ =**

(1/3) ·

| qM⁽ⁿ⁻¹⁾    | 3⁻⁽ⁿ⁻¹⁾J_N | 3⁻⁽ⁿ⁻¹⁾J_N |
| ---------- | ---------- | ---------- |
| 3⁻⁽ⁿ⁻¹⁾J_N | qM⁽ⁿ⁻¹⁾    | 3⁻⁽ⁿ⁻¹⁾J_N |
| 3⁻⁽ⁿ⁻¹⁾J_N | 3⁻⁽ⁿ⁻¹⁾J_N | qM⁽ⁿ⁻¹⁾    |

Початкова умова:

M⁽⁰⁾ = [c_q].

Ця рекурсія точно відтворює матрицю W8.

### Чому це важливо

1. Не потрібно повторно обчислювати всі спільні префікси.
2. Структура дерева безпосередньо відображається у структурі матриці.
3. Можна будувати рекурсивні алгоритми множення на вектор.
4. Можна використовувати блокову діагоналізацію.
5. Можна незалежно перевіряти рекурсивну та пряму реалізації.

**Рекомендація:** додати рекурсивну побудову матриці до W10 як обов'язковий алгоритмічний варіант.

Не варто обмежувати реалізацію повним зберіганням щільної матриці.

Для великих n це буде головним обчислювальним обмеженням.

---

# 8. Незалежна чисельна перевірка

Я провів контрольне чисельне обчислення для трьох значень q:

* q = 0.2;
* q = 0.7;
* q = 0.99.

Для кожного значення побудовано матриці рівнів n = 1, 2, 3 та порівняно їхні чисельні власні значення з аналітичними формулами.

Результат:

|    q |  n | Максимальна абсолютна похибка власних значень |
| ---: | -: | --------------------------------------------: |
|  0.2 |  1 |                                 ≈ 5.6 × 10⁻¹⁷ |
|  0.2 |  2 |                                 ≈ 1.2 × 10⁻¹⁶ |
|  0.2 |  3 |                                 ≈ 3.3 × 10⁻¹⁶ |
|  0.7 |  1 |                                 ≈ 1.1 × 10⁻¹⁶ |
|  0.7 |  2 |                                 ≈ 2.2 × 10⁻¹⁶ |
|  0.7 |  3 |                                 ≈ 1.2 × 10⁻¹⁵ |
| 0.99 |  1 |                                 ≈ 9.7 × 10⁻¹⁷ |
| 0.99 |  2 |                                 ≈ 1.3 × 10⁻¹⁶ |
| 0.99 |  3 |                                 ≈ 3.3 × 10⁻¹⁶ |

Додатково перевірено сталість сум рядків. Максимальна похибка також перебуває приблизно на рівні 10⁻¹⁶.

### Інтерпретація

Ці результати підтверджують, що:

* формула матриці W8 узгоджується зі спектральними формулами W7;
* кратності власних значень узгоджуються з розмірністю Hₙ;
* чисельні результати відповідають теоретичним формулам у межах похибки подвійної точності.

Але це **контрольна чисельна перевірка**, а не формальна верифікація всієї специфікації.

Вона також не підтверджує коректність будь-якої зовнішньої реалізації SUBIT-WARP, якщо її код окремо не перевірено.

---

# 9. V5 — Formal Verification: Lean

Формальну верифікацію я рекомендую виконувати поступово.

Не варто починати з формалізації всього нескінченновимірного спектрального оператора. Це значно ускладнить роботу й ускладнить локалізацію помилок.

Краще побудувати п'ять рівнів формальних зобов'язань.

### Рівень F1 — Discrete Structure

Формалізувати:

* алфавіт B;
* скінченні адреси;
* довжину адреси;
* спільний префікс;
* кількість адрес рівня n;
* рекурсивне розбиття циліндрів.

Це найпростіший рівень.

### Рівень F2 — Metric Structure

Довести:

* симетричність;
* невід'ємність;
* розділення точок;
* ультраметричну нерівність;
* еквівалентність метрик dᵥ та d_S за умови αᵥ > 0.

### Рівень F3 — Finite Matrix

Формалізувати M⁽ⁿ⁾ як скінченну матрицю.

Довести:

* симетричність;
* суму рядків;
* власне значення c_q;
* спектральну декомпозицію за рівнями;
* кратності власних значень.

Тут можна використати скінченновимірну лінійну алгебру та рекурсивну структуру матриці.

### Рівень F4 — Infinite Operator

Формалізувати:

* простір L²(Σ,μ);
* ядро K_q;
* інтегральний оператор T_q;
* самоспряженість;
* компактність;
* ортогональний розклад H = ⊕Wⱼ.

Це вже суттєво складніший рівень.

### Рівень F5 — Spectral Theorems

Довести:

* формули λⱼ та τⱼ;
* повний спектр L_q;
* відсутність власного значення −c_q;
* точну операторну похибку;
* збіжність скінченних спектрів.

Для цього рівня знадобиться формальна робота з компактними самоспряженими операторами та спектральною теорією.

### Важливе обмеження

Я не стверджую, що ці докази вже реалізовані в Lean.

Наведений поділ — це план формалізації та реєстр математичних зобов'язань, а не звіт про наявні Lean-артефакти.

---

# 10. Виправлена редакція W10 для специфікації

Нижче — готова редакція W10, яку рекомендую включити до SUBIT-WARP v0.3.

## W10. COMPUTATIONAL AND FORMAL VERIFICATION

**Status:** VERIFICATION FRAMEWORK DEFINED · IMPLEMENTATION NOT CERTIFIED.

### W10.1. Verification architecture

The verification framework consists of five independent layers:

* V1 — Structural Verification.
* V2 — Metric Verification.
* V3 — Operator Verification.
* V4 — Spectral Verification.
* V5 — Formal Verification.

Each layer has independent verification obligations.

Numerical verification, mathematical proof, and formal verification must be reported as distinct statuses.

### W10.2. Structural verification

The implementation must verify:

1. |Bⁿ| = 3ⁿ.
2. Each address has exactly three children.
3. μ(Cσ) = 3⁻ⁿ.
4. Σ|σ|=n μ(Cσ) = 1.
5. Cσ = Cσ1 ∪ Cσ2 ∪ Cσ3.
6. The three child cylinders are pairwise disjoint.
7. The common-prefix function satisfies its defining bounds.

All finite structural tests must use exact combinatorial checks.

### W10.3. Metric verification

The implementation must verify the consistency of:

d_S(ξ,η) = 2⁻ˡ(ξ,η),

dᵥ(ξ,η) = exp(−αᵥℓ(ξ,η)).

The parameter condition is:

αᵥ > 0.

The metric relation is:

dᵥ = d_S^(αᵥ/ln 2).

The Hausdorff dimension is:

Dᵥ = ln 3/αᵥ.

The ultrametric inequality must be established mathematically and may additionally be tested on finite samples.

Randomized testing does not replace the universal proof.

### W10.4. Operator verification

For:

K_q(ξ,η) = q^ℓ(ξ,η), ξ ≠ η,

K_q(ξ,ξ) = 0,

and:

0 < q < 1,

the verification framework must establish:

1. Kernel symmetry.
2. Kernel boundedness.
3. Square integrability.
4. Self-adjointness of T_q.
5. Compactness of T_q.
6. The row integral c_q = 2/(3 − q).
7. The action of T_q on constant functions.

The implementation must not assert that T_q is positive semidefinite.

The normalized operator:

L_q = T_q − c_qI

is negative semidefinite.

### W10.5. Finite matrix verification

For each finite level n, construct:

Mστ⁽ⁿ⁾ = 3⁻ⁿ Avg(Cσ × Cτ, q^ℓ).

The exact entries are:

Mστ⁽ⁿ⁾ = 3⁻ⁿqⁿc_q, if σ = τ,

Mστ⁽ⁿ⁾ = 3⁻ⁿqᵏ, if σ ≠ τ and k = ℓ(σ,τ).

The implementation must verify:

* Matrix symmetry.
* Constant row sum c_q.
* Dimension 3ⁿ.
* Exact finite-level spectrum.
* Spectral multiplicities.

### W10.6. Recursive matrix construction

Define:

M⁽⁰⁾ = [c_q].

For n ≥ 1, let N = 3ⁿ⁻¹ and let J_N denote the all-ones matrix.

Then:

M⁽ⁿ⁾ = (1/3) ·

[ qM⁽ⁿ⁻¹⁾       3⁻⁽ⁿ⁻¹⁾J_N   3⁻⁽ⁿ⁻¹⁾J_N
3⁻⁽ⁿ⁻¹⁾J_N    qM⁽ⁿ⁻¹⁾      3⁻⁽ⁿ⁻¹⁾J_N
3⁻⁽ⁿ⁻¹⁾J_N    3⁻⁽ⁿ⁻¹⁾J_N   qM⁽ⁿ⁻¹⁾ ]

The recursive construction must be tested against the direct cylinder-based construction at small levels.

### W10.7. Spectral verification

The finite-level spectrum must satisfy:

Spec(M⁽ⁿ⁾) = {c_q} ∪ {λⱼ(q) : 1 ≤ j ≤ n},

where:

λⱼ(q) = −(1 − q)qʲ⁻¹/[3ʲ⁻¹(3 − q)].

The multiplicities are:

mult(c_q) = 1,

mult(λⱼ) = 2·3ʲ⁻¹.

The normalized finite-level spectrum is:

Spec(L_q⁽ⁿ⁾) = {0} ∪ {τⱼ(q) : 1 ≤ j ≤ n}.

The multiplicity sum must equal:

1 + Σⱼ₌₁ⁿ 2·3ʲ⁻¹ = 3ⁿ.

### W10.8. Error verification

The exact operator-norm error is:

‖T_q − PₙT_qPₙ‖ = (1 − q)qⁿ/[3ⁿ(3 − q)].

The exact spectral Hausdorff error is:

d_H(Spec(L_q⁽ⁿ⁾), Spec(L_q))
= (1 − q)qⁿ⁻¹/[3ⁿ⁻¹(3 − q)].

The implementation must verify both formulas independently.

The finite-dimensional zero extension of L_q⁽ⁿ⁾ must not be reported as an operator-norm convergent approximation of L_q.

### W10.9. Parameter verification

The primary parameters satisfy:

αᵥ > 0,

α𝑤 > 0.

Derived parameters:

q = exp(−α𝑤),

β = α𝑤/αᵥ,

Dᵥ = ln 3/αᵥ.

The implementation must reject inconsistent parameter configurations.

The inverse kernel integrability condition is:

β < Dᵥ.

This condition does not restrict integrability of the ordinary decaying kernel K_q.

### W10.10. Formal verification roadmap

Formalization should proceed in five stages:

F1 — Discrete tree and cylinder structure.

F2 — Ultrametric and Hausdorff geometry.

F3 — Finite matrices and their exact spectra.

F4 — Infinite-dimensional integral operator.

F5 — Compact spectral theory and convergence theorems.

Each formally verified result must be accompanied by its theorem statement and the corresponding proof artifact.

A mathematical proof in the specification must not be labeled Lean-verified without a completed formal proof.

### W10.11. Numerical verification policy

Numerical tests must record:

* Parameter values.
* Tree depth.
* Matrix construction method.
* Numerical precision.
* Solver used.
* Absolute and relative tolerances.
* Observed residuals.
* Expected analytical values.

Eigenvalue comparisons must account for multiplicities and numerical degeneracy.

For small n, direct dense matrices may be used.

For larger n, recursive or matrix-free methods are preferred.

### W10.12. Verification status vocabulary

Every theorem and test must have one of the following statuses:

* PROVED — mathematical proof established.
* FORMALLY VERIFIED — proof checked by a formal proof assistant.
* NUMERICALLY VERIFIED — numerical test completed successfully.
* CONDITIONAL — depends on explicitly listed assumptions.
* OPEN — not yet established.
* FALSE — contradicted by the mathematical model.

A single result may carry more than one status, but these statuses must not be conflated.

### W10.13. Acceptance criteria

W10 is accepted as a verification framework when:

1. All mathematical invariants are specified.
2. All finite-level matrix tests are defined.
3. Recursive and direct matrix constructions are cross-checkable.
4. Exact spectral formulas are included.
5. Exact error formulas are included.
6. Parameter consistency checks are defined.
7. Formalization obligations are separated from numerical tests.
8. No unverified implementation is represented as certified.

**W10 conclusion:** The verification framework establishes a reproducible route from the finite combinatorial structure to the infinite spectral model, while preserving the distinction between mathematical proof, numerical evidence, and formal certification.

---

# 11. Оновлений Verification Registry

Після аудиту W10 пропоную використовувати такий реєстр.

| ID       | Твердження                  | Математичний статус | Чисельний статус                                | Lean |
| -------- | --------------------------- | ------------------- | ----------------------------------------------- | ---- |
| W10-STR  | Структура адрес і циліндрів | PROVED              | Частково перевірено                             | OPEN |
| W10-MET  | Ультраметрика               | PROVED              | Частково перевірено                             | OPEN |
| W10-DIM  | Розмірність межі            | PROVED              | Не потрібно для доказу                          | OPEN |
| W10-KER  | Властивості ядра            | PROVED              | Частково перевірено                             | OPEN |
| W10-COM  | Компактність T_q            | PROVED              | Не замінюється тестом                           | OPEN |
| W10-MAT  | Точна матриця M⁽ⁿ⁾          | PROVED              | Перевірено n = 1–3                              | OPEN |
| W10-EIG  | Скінченний спектр           | PROVED              | Перевірено n = 1–3                              | OPEN |
| W10-ERR  | Операторна похибка          | PROVED              | Формула визначена; чисельна серія не перевірена | OPEN |
| W10-SPEC | Спектральна похибка         | PROVED              | Формула визначена; чисельна серія не перевірена | OPEN |
| W10-PAR  | Узгодженість параметрів     | PROVED              | Частково перевірено                             | OPEN |
| W10-REC  | Рекурсивна матриця          | PROVED              | Потрібна окрема реалізація                      | OPEN |

Чисельна перевірка матриць n = 1–3 є фактично виконаною контрольною перевіркою. Вона не означає, що весь W10 уже реалізовано.

---

# 12. Критичні рекомендації для наступної версії

Я б не називав SUBIT-WARP v0.3 завершеною стабільною версією. Правильніший статус:

**DRAFT · MATHEMATICALLY REFINED · NUMERICALLY SPOT-CHECKED · NOT FORMALLY VERIFIED**

Перед переходом до v0.4 потрібно виконати ще чотири завдання:

1. Додати рекурсивну реалізацію M⁽ⁿ⁾ та перевірити її проти прямої побудови.
2. Побудувати повний автоматизований тестовий набір для n = 1,…,N.
3. Формалізувати скінченнорівневий спектральний результат у Lean.
4. Провести заключний аудит W0–W10 на несуперечність позначень, областей визначення та статусів теорем.

Особливо рекомендую спочатку формалізувати **скінченну спектральну декомпозицію**, а вже потім переходити до нескінченновимірного оператора. Це дасть перевірювану математичну основу для програмної реалізації.

---

## 13. Наступний етап: інтегральний аудит W0–W10

На цьому етапі ми перевірили кожен основний компонент окремо. Але окремо правильні теореми ще не гарантують, що вся специфікація узгоджена як єдина система.

Залишаються чотири особливо важливі питання:

* Чи всі означення використовують одну й ту саму міру μ?
* Чи немає суперечностей між геометрією межі та умовами W5?
* Чи правильно пов'язано спектральний оператор із параметризацією W9?
* Чи не використовує W8 результати W7 за умов, які в самій специфікації не були явно встановлені?

**Моя рекомендація — наступним кроком провести інтегральний аудит W0–W10: theorem dependency graph, consistency matrix, реєстр прихованих припущень та остаточний список блокерів перед SUBIT-WARP v0.4.** Це буде важливіше за додавання нових математичних модулів: спочатку потрібно переконатися, що вже побудована система справді замкнена й несуперечлива.
