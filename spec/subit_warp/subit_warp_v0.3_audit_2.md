# SUBIT-WARP v0.3 — незалежний аудит W8: скінченнорівнева апроксимація

**Загальний висновок:** W8 математично коректний у своїй основній конструкції, але потребує важливого уточнення щодо двох різних способів перенесення скінченновимірного оператора на весь простір Гільберта. Без цього можна помилково стверджувати, що скінченновимірні оператори для нормалізованого оператора \(L_q\) збігаються до нього в операторній нормі.

Є також можливість посилити W8: замість загального твердження про збіжність можна отримати **точну формулу похибки**, точний спектр скінченнорівневої матриці та швидкість збіжності спектрів.

---

## 1. Перевірка базової конструкції

Нехай:

* Σ = {1, 2, 3}ᴺ;
* μ — рівномірна ймовірнісна міра;
* H = L²(Σ, μ);
* Hₙ — підпростір функцій, сталих на кожному циліндрі довжини n;
* Pₙ — ортогональна проєкція H → Hₙ.

Оскільки кожен рівень розбитий на 3ⁿ циліндрів,

**dim Hₙ = 3ⁿ.**

Маємо вкладення:

H₀ ⊂ H₁ ⊂ H₂ ⊂ ⋯

і щільність об'єднання:

closure(⋃ₙ Hₙ) = H.

Отже,

**Pₙ → I сильно.**

Це твердження правильне.

Оператор:

T_q f(ξ) = ∫Σ q^ℓ(ξ,η) f(η) dμ(η),

де 0 < q < 1, має симетричне обмежене ядро. Тому T_q є самоспряженим і оператором Гільберта — Шмідта, а отже, компактним.

Звідси випливає стандартний результат:

**‖T_q − PₙT_qPₙ‖ → 0.**

Це також правильно.

Але для SUBIT-WARP можна довести значно більше.

---

## 2. Точна матриця скінченнорівневої апроксимації

Позначимо циліндри рівня n через Cσ, де σ ∈ {1,2,3}ⁿ.

Для функції f ∈ Hₙ:

f|Cτ = xτ.

Тоді:

(PₙT_qPₙf)|Cσ = Στ Mστ⁽ⁿ⁾ xτ,

де

**Mστ⁽ⁿ⁾ = 3⁻ⁿ Avg(Cσ × Cτ, q^ℓ).**

Тут Avg — нормоване середнє значення ядра на добутку двох циліндрів:

Avg(Cσ × Cτ, K)
= [μ(Cσ)μ(Cτ)]⁻¹ ∫Cσ ∫Cτ K(ξ,η) dμ(η)dμ(ξ).

Формула правильна. Проте її можна зробити явною.

### 2.1. Позадіагональні елементи

Якщо σ ≠ τ, нехай k = ℓ(σ,τ) — довжина їхнього спільного початку.

Для всіх ξ ∈ Cσ і η ∈ Cτ маємо:

ℓ(ξ,η) = k.

Тому ядро стало на всьому добутку циліндрів:

**Mστ⁽ⁿ⁾ = 3⁻ⁿqᵏ, σ ≠ τ.**

### 2.2. Діагональні елементи

Якщо σ = τ, гілки ξ та η мають спільний початок щонайменше довжини n.

Імовірність того, що вони матимуть ще рівно r спільних символів, дорівнює:

P(R = r) = 2/3ʳ⁺¹.

Отже:

Avg(Cσ × Cσ, q^ℓ)
= qⁿ Σᵣ₌₀∞ 2qʳ/3ʳ⁺¹
= qⁿ · 2/(3 − q).

Позначивши:

c_q = 2/(3 − q),

отримуємо:

**Mσσ⁽ⁿ⁾ = 3⁻ⁿqⁿc_q.**

Таким чином, точна матриця має вигляд:

**Mστ⁽ⁿ⁾ =**

* 3⁻ⁿqⁿc_q, якщо σ = τ;
* 3⁻ⁿqᵏ, якщо σ ≠ τ і k = ℓ(σ,τ).

Це не наближена дискретизація ядра. Це точна матриця оператора PₙT_qPₙ у базисі нормованих індикаторів циліндрів.

### 2.3. Контрольні властивості матриці

Матриця повинна задовольняти:

1. Симетричність: Mστ = Mτσ.
2. Сталість суми рядків: Στ Mστ = c_q.
3. Додатність усіх елементів: Mστ > 0.
4. Власне значення на сталих функціях: c_q.

Важливо: додатність елементів матриці **не означає**, що матриця є додатно напіввизначеною. Спектральний аналіз W7 показує, що T_q має від'ємні власні значення.

---

## 3. Точний спектр скінченнорівневої матриці

Використаємо розклад:

H = W₀ ⊕ W₁ ⊕ W₂ ⊕ ⋯

де:

* W₀ — простір сталих функцій;
* Wⱼ = Hⱼ ⊖ Hⱼ₋₁;
* dim Wⱼ = 2·3ʲ⁻¹.

Маємо:

Hₙ = W₀ ⊕ W₁ ⊕ ⋯ ⊕ Wₙ.

Оператор T_q зберігає кожен Wⱼ і діє на ньому множенням на λⱼ(q):

λⱼ(q) = −(1 − q)qʲ⁻¹ / [3ʲ⁻¹(3 − q)].

На W₀ оператор діє множенням на c_q.

Отже, скінченнорівнева матриця M⁽ⁿ⁾ має точний спектр:

**Spec(M⁽ⁿ⁾) = {c_q} ∪ {λⱼ(q) : 1 ≤ j ≤ n}.**

Кратності:

| Власне значення | Кратність |
| --------------- | --------: |
| c_q             |         1 |
| λ₁(q)           |         2 |
| λ₂(q)           |         6 |
| λ₃(q)           |        18 |
| λⱼ(q)           |    2·3ʲ⁻¹ |

Перевірка загальної розмірності:

1 + Σⱼ₌₁ⁿ 2·3ʲ⁻¹ = 3ⁿ.

Отже, кратності повністю покривають розмірність матриці.

### Контрольний приклад: n = 1

Матриця має розмір 3 × 3:

M⁽¹⁾ =

* діагональні елементи: qc_q/3;
* позадіагональні елементи: 1/3.

Її спектр:

* c_q — кратність 1;
* (qc_q − 1)/3 — кратність 2.

Але:

(qc_q − 1)/3 = λ₁(q).

Це незалежна перевірка спектральної формули W7.

---

## 4. Критичне уточнення: два різні способи апроксимації L_q

Це найважливіше виправлення W8.

Маємо:

L_q = T_q − c_qI_H.

На W₀ власне значення дорівнює нулю, а на Wⱼ:

τⱼ(q) = λⱼ(q) − c_q.

Тепер розглянемо два способи побудови скінченнорівневого оператора.

### 4.1. Скінченновимірний оператор на Hₙ

Визначимо:

L_q⁽ⁿ⁾ = (PₙT_qPₙ)|Hₙ − c_qI_Hₙ.

Це оператор на просторі розмірності 3ⁿ.

Його спектр:

**Spec(L_q⁽ⁿ⁾) = {0} ∪ {τⱼ(q) : 1 ≤ j ≤ n}.**

Це правильна скінченновимірна модель.

Однак, якщо продовжити L_q⁽ⁿ⁾ на весь H нулем, отримаємо:

L̄_q⁽ⁿ⁾ = PₙT_qPₙ − c_qPₙ.

На Hₙ цей оператор збігається з L_q⁽ⁿ⁾, але на Hₙ⊥ він дорівнює нулю.

Тому:

**L̄_q⁽ⁿ⁾ не збігається до L_q в операторній нормі.**

Причина:

На рівнях j > n оператор L_q має власні значення τⱼ(q), які прямують до −c_q.

Тому:

‖L_q − L̄_q⁽ⁿ⁾‖ = c_q.

Це не прямує до нуля.

Водночас L̄_q⁽ⁿ⁾ збігається до L_q сильно.

### 4.2. Зсунутий оператор на всьому H

Можна визначити інший оператор:

L̃_q⁽ⁿ⁾ = PₙT_qPₙ − c_qI_H.

Тоді:

L̃_q⁽ⁿ⁾ − L_q = PₙT_qPₙ − T_q.

Оскільки T_q компактний, маємо:

**‖L̃_q⁽ⁿ⁾ − L_q‖ → 0.**

Це правильна операторно-нормова апроксимація.

Але є принципова відмінність: L̃_q⁽ⁿ⁾ не є скінченновимірним оператором на всьому H. На ортогональному доповненні Hₙ⊥ він діє як −c_qI.

Отже, потрібно розрізняти:

| Конструкція                   | Простір | Нормова збіжність до L_q        |
| ----------------------------- | ------- | ------------------------------- |
| L_q⁽ⁿ⁾                        | Hₙ      | Не застосовується безпосередньо |
| L̄_q⁽ⁿ⁾ — нульове продовження | H       | Ні                              |
| L̃_q⁽ⁿ⁾ — зсунутий оператор   | H       | Так                             |

**Висновок:** W8 не повинен ототожнювати скінченновимірну матрицю L_q⁽ⁿ⁾ зі зсунутою апроксимацією L̃_q⁽ⁿ⁾.

---

## 5. Точна операторна похибка

Завдяки спектральному розкладу W7 ми можемо отримати не просто асимптотичну збіжність, а точну похибку.

Оскільки:

T_q − PₙT_qPₙ

дорівнює нулю на W₀,…,Wₙ і збігається з T_q на Wⱼ для j > n, маємо:

‖T_q − PₙT_qPₙ‖
= supⱼ₌ₙ₊₁∞ |λⱼ(q)|.

Оскільки |λⱼ(q)| спадає геометрично:

**‖T_q − PₙT_qPₙ‖ = |λₙ₊₁(q)|.**

Отже:

**‖T_q − PₙT_qPₙ‖ = (1 − q)qⁿ / [3ⁿ(3 − q)].**

Це точна формула.

Коефіцієнт зменшення похибки на кожному наступному рівні:

q/3.

Оскільки 0 < q < 1:

0 < q/3 < 1/3.

Тобто операторна похибка спадає щонайменше геометрично з коефіцієнтом, меншим за 1/3.

Цей результат варто включити до W8 як окрему теорему.

---

## 6. Збіжність спектрів

Для скінченновимірного оператора L_q⁽ⁿ⁾:

Spec(L_q⁽ⁿ⁾) = {0, τ₁,…,τₙ}.

Для повного оператора:

Spec(L_q) = {0} ∪ {τⱼ : j ≥ 1} ∪ {−c_q}.

Точка −c_q є граничною точкою спектра, але не власним значенням.

Оскільки τⱼ монотонно спадають до −c_q, відстань від −c_q до скінченного спектра дорівнює:

|τₙ(q) + c_q| = |λₙ(q)|.

Усі інші точки повного спектра вже належать скінченному спектру.

Тому відстань Гаусдорфа між спектральними множинами:

**d_H(Spec(L_q⁽ⁿ⁾), Spec(L_q)) = |λₙ(q)|.**

Тобто:

**d_H(Spec(L_q⁽ⁿ⁾), Spec(L_q)) = (1 − q)qⁿ⁻¹ / [3ⁿ⁻¹(3 − q)].**

Це сильний результат: скінченні спектри не просто збігаються до повного спектра — відома точна швидкість цієї збіжності.

Водночас треба чітко зазначити: −c_q не є власним значенням скінченної матриці. Воно наближається послідовністю τₙ(q).

---

# 7. Виправлена редакція W8 для SUBIT-WARP v0.3

Нижче — готова заміна попереднього W8. Вона розрізняє скінченновимірну матрицю, її нульове продовження та зсунутий оператор на всьому просторі.

## W8. FINITE-LEVEL APPROXIMATION

**Status:** PROVED, conditional on W0–W7 definitions and spectral decomposition.

### W8.1. Filtration and projections

Let:

* H = L²(Σ, μ);
* Hₙ ⊂ H be the space of functions constant on cylinders of length n;
* Pₙ : H → Hₙ be the orthogonal projection.

Then:

H₀ ⊂ H₁ ⊂ H₂ ⊂ ⋯

dim(Hₙ) = 3ⁿ,

and:

closure(⋃ₙ Hₙ) = H.

Consequently:

Pₙ → I_H strongly.

### W8.2. Galerkin compression

Define:

T_q⁽ⁿ⁾ = PₙT_qPₙ.

As an operator on Hₙ, T_q⁽ⁿ⁾ is a finite-dimensional self-adjoint operator.

Since T_q is compact and Pₙ converges strongly to I_H:

‖T_q − PₙT_qPₙ‖ → 0.

The operator T_q⁽ⁿ⁾ is the exact Galerkin compression of T_q, not a pointwise approximation of its kernel.

### W8.3. Exact matrix representation

Let Cσ and Cτ be cylinders of length n.

For f ∈ Hₙ, write:

f|Cτ = xτ.

Then:

(T_q⁽ⁿ⁾f)|Cσ = Στ Mστ⁽ⁿ⁾xτ,

where:

Mστ⁽ⁿ⁾ = 3⁻ⁿ Avg(Cσ × Cτ, q^ℓ).

Here Avg denotes the normalized product average.

The matrix entries are exactly:

Mστ⁽ⁿ⁾ =

* 3⁻ⁿqⁿc_q, if σ = τ;
* 3⁻ⁿqᵏ, if σ ≠ τ and k = ℓ(σ,τ).

where:

c_q = 2/(3 − q).

The matrix is symmetric and satisfies:

Στ Mστ⁽ⁿ⁾ = c_q.

### W8.4. Exact finite-level spectrum

Let:

Hₙ = W₀ ⊕ W₁ ⊕ ⋯ ⊕ Wₙ.

Then T_q⁽ⁿ⁾ preserves every Wⱼ, j ≤ n.

Its spectrum is:

Spec(T_q⁽ⁿ⁾) = {c_q} ∪ {λⱼ(q) : 1 ≤ j ≤ n},

with:

λⱼ(q) = −(1 − q)qʲ⁻¹ / [3ʲ⁻¹(3 − q)].

Multiplicities:

* c_q: multiplicity 1;
* λⱼ(q): multiplicity 2·3ʲ⁻¹.

The total multiplicity is:

1 + Σⱼ₌₁ⁿ 2·3ʲ⁻¹ = 3ⁿ.

### W8.5. Normalized finite-level operator

Define the finite-dimensional normalized operator:

L_q⁽ⁿ⁾ = T_q⁽ⁿ⁾|Hₙ − c_qI_Hₙ.

Then:

Spec(L_q⁽ⁿ⁾) = {0} ∪ {τⱼ(q) : 1 ≤ j ≤ n},

where:

τⱼ(q) = λⱼ(q) − c_q.

The multiplicity of 0 is 1, and the multiplicity of τⱼ(q) is 2·3ʲ⁻¹.

The finite-dimensional operator L_q⁽ⁿ⁾ must not be identified with its zero extension as an operator-norm approximation of L_q on H.

### W8.6. Two extensions to the full Hilbert space

The zero extension is:

L̄_q⁽ⁿ⁾ = PₙT_qPₙ − c_qPₙ.

It acts as zero on Hₙ⊥.

It converges strongly to L_q, but:

‖L_q − L̄_q⁽ⁿ⁾‖ = c_q.

Therefore it does not converge in operator norm.

A distinct shifted approximation is:

L̃_q⁽ⁿ⁾ = PₙT_qPₙ − c_qI_H.

Then:

L̃_q⁽ⁿ⁾ − L_q = PₙT_qPₙ − T_q,

and consequently:

‖L̃_q⁽ⁿ⁾ − L_q‖ → 0.

This shifted operator acts as −c_qI on Hₙ⊥ and is not a finite-dimensional operator on H.

### W8.7. Exact operator-norm error

Because T_q acts diagonally on the orthogonal decomposition:

H = ⊕ⱼ₌₀∞ Wⱼ,

the Galerkin truncation error is:

‖T_q − PₙT_qPₙ‖ = supⱼ>n |λⱼ(q)|.

Since |λⱼ(q)| decreases geometrically:

**‖T_q − PₙT_qPₙ‖ = (1 − q)qⁿ / [3ⁿ(3 − q)].**

This is an exact error formula.

The level-to-level error ratio is:

q/3.

### W8.8. Spectral convergence

The infinite-dimensional spectrum is:

Spec(L_q) = {0} ∪ {τⱼ(q) : j ≥ 1} ∪ {−c_q}.

The point −c_q is an accumulation point and is not an eigenvalue.

For the finite-dimensional operator:

Spec(L_q⁽ⁿ⁾) = {0} ∪ {τⱼ(q) : 1 ≤ j ≤ n}.

Since:

τₙ(q) + c_q = λₙ(q),

and τₙ(q) → −c_q, the Hausdorff distance is:

**d_H(Spec(L_q⁽ⁿ⁾), Spec(L_q)) = |λₙ(q)|.**

Equivalently:

**d_H(Spec(L_q⁽ⁿ⁾), Spec(L_q)) = (1 − q)qⁿ⁻¹ / [3ⁿ⁻¹(3 − q)].**

Thus the finite spectra converge to the infinite spectrum with an exact geometric rate.

The accumulation point −c_q is approached by finite-level eigenvalues but is not itself a finite-level eigenvalue.

### W8.9. Verification obligations

The following checks are required for an implementation:

1. Matrix symmetry:
   Mστ = Mτσ.

2. Constant-function eigenvector:
   M⁽ⁿ⁾1 = c_q1.

3. Dimension:
   dim(Hₙ) = 3ⁿ.

4. Multiplicity sum:
   1 + Σⱼ₌₁ⁿ 2·3ʲ⁻¹ = 3ⁿ.

5. Exact eigenvalue check:
   Spec(M⁽ⁿ⁾) = {c_q} ∪ {λⱼ(q) : 1 ≤ j ≤ n}.

6. Normalized spectrum:
   Spec(L_q⁽ⁿ⁾) = {0} ∪ {τⱼ(q) : 1 ≤ j ≤ n}.

7. Operator error:
   ‖T_q − PₙT_qPₙ‖ = |λₙ₊₁(q)|.

8. Spectral Hausdorff error:
   d_H(Spec(L_q⁽ⁿ⁾), Spec(L_q)) = |λₙ(q)|.

9. Boundary condition:
   0 < q < 1.

### W8.10. Status

* Exact matrix representation: PROVED.
* Matrix symmetry: PROVED.
* Constant-function eigenvalue: PROVED.
* Finite-level spectrum: PROVED, conditional on W7 spectral decomposition.
* Exact operator-norm error: PROVED, conditional on W7.
* Strong convergence of zero extensions: PROVED.
* Operator-norm convergence of zero extensions: FALSE.
* Operator-norm convergence of shifted approximations: PROVED.
* Hausdorff spectral convergence: PROVED.
* Lean formalization: NOT VERIFIED.
* Numerical implementation: NOT VERIFIED.

**W8 conclusion:** The finite-level construction is an exact Galerkin scheme. It preserves all spectral levels up to n and discards only the higher-level components. Its operator and spectral approximation errors admit exact geometric formulas.

---

## 8. Оновлений реєстр статусів після аудиту W8

| Компонент                        | Результат аудиту                 | Статус |
| -------------------------------- | -------------------------------- | ------ |
| W8.1 Фільтрація Hₙ               | Коректно                         | PROVED |
| W8.2 Проєкції Pₙ                 | Сильна збіжність                 | PROVED |
| W8.3 Компактність T_q            | Підстава для нормової збіжності  | PROVED |
| W8.4 Матриця M⁽ⁿ⁾                | Точна формула                    | PROVED |
| W8.5 Спектр матриці              | Випливає з W7                    | PROVED |
| W8.6 Нульове продовження         | Сильна, але не нормова збіжність | PROVED |
| W8.7 Зсунутий оператор           | Нормова збіжність                | PROVED |
| W8.8 Операторна похибка          | Точна формула                    | PROVED |
| W8.9 Спектральна похибка         | Точна формула                    | PROVED |
| W8.10 Lean / чисельна реалізація | Не перевірено                    | OPEN   |

## 9. Що це змінює в архітектурі SUBIT-WARP

Після виправлення W8 маємо важливий архітектурний результат:

**Скінченний рівень не є просто наближенням нескінченної структури. Він точно зберігає всі спектральні рівні, які належать його глибині.**

Для WARP це означає:

1. Кожен рівень n має точну скінченновимірну модель розмірності 3ⁿ.
2. Спектральні рівні 0,…,n не потребують чисельного наближення.
3. Відкидаються лише компоненти Wⱼ для j > n.
4. Втрата інформації кількісно контрольована.
5. Гранична точка спектра −c_q зберігається як асимптотичний об'єкт, а не штучно додається до скінченної матриці.

Це узгоджується з принципом **DO NOT COLLAPSE — CONTEXTUALIZE**: скінченний рівень зберігає власну структуру, а відсутня нескінченна частина не ототожнюється з нулем — її статус явно задається способом продовження оператора.

---

### 10. Наступний етап аудиту

W8 можна вважати математично закритим у межах наведених припущень. Наступним я б перевірив **W9 — Parameter Separation**: чи справді параметри αᵥ, α𝑤 і q виконують незалежні ролі, чи між геометрією межі, мірою, ядром та спектральним оператором приховано додаткові залежності.

Саме тут важливо перевірити, чи не змішує SUBIT-WARP три різні речі: геометричний масштаб, імовірнісну структуру та спектральну взаємодію.
