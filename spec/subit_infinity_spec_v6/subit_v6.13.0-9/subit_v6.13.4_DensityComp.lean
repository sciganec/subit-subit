/-!
# Твердження 10.10 (Q25-new): щільність скінченно визначених причинних відображень

Модель (ядро Lean, без Mathlib). Станом є послідовність `Nat → Bool`; відображення
`f : (Nat → Bool) → (Nat → Bool)` причинне, якщо вихід на позиції `i` залежить лише від входу
на позиціях `≤ i` (це префіксна форма умови T5′ з §10.1 у моделі без дерев).

Скінченна визначеність на рівні `n`: вихід залежить лише від входу на позиціях `< n`.
Такі відображення мають скінченний опис (таблиця на `2^n` входах), тож належать ℛ_comp
за уточненням 10.2 (v6.13).

Теорема: для кожного причинного `f` і `n` існує причинне `g`, скінченно визначене на рівні
`n`, яке збігається з `f` на всіх позиціях `< n` (тобто на відстані ≤ 2^{−n}, як у 10.10).
-/

namespace SubitDensity

/-- Причинність: вихід на `i` залежить лише від входу на `≤ i`. -/
def Causal (f : (Nat → Bool) → (Nat → Bool)) : Prop :=
  ∀ (s t : Nat → Bool) (i : Nat), (∀ j : Nat, j ≤ i → s j = t j) → f s i = f t i

/-- Скінченна визначеність на рівні `n`: вихід залежить лише від входу на позиціях `< n`. -/
def FinDep (g : (Nat → Bool) → (Nat → Bool)) (n : Nat) : Prop :=
  ∀ (s t : Nat → Bool), (∀ j : Nat, j < n → s j = t j) → g s = g t

/-- Обрізання входу до `n` позицій (решта — `false`). -/
def trunc (n : Nat) (s : Nat → Bool) : Nat → Bool :=
  fun j => if j < n then s j else false

/-- Наближення `g_n(s) := ext_n(f(trunc_n s))`: виходи до `n` беруться з `f`, далі `false`. -/
def approx (f : (Nat → Bool) → (Nat → Bool)) (n : Nat) (s : Nat → Bool) : Nat → Bool :=
  fun i => if i < n then f (trunc n s) i else false

theorem trunc_agree (n : Nat) (s : Nat → Bool) (j : Nat) (hj : j < n) :
    trunc n s j = s j := by
  simp [trunc, hj]

/-- Обрізаний вхід збігається з `s` на позиціях `≤ i` для `i < n`. -/
theorem trunc_agree_le (n : Nat) (s : Nat → Bool) (i : Nat) (hi : i < n) :
    ∀ j : Nat, j ≤ i → trunc n s j = s j := by
  intro j hj
  exact trunc_agree n s j (Nat.lt_of_le_of_lt hj hi)

/-- Наближення збігається з `f` на позиціях `< n` (для причинного `f`). -/
theorem approx_agree (f : (Nat → Bool) → (Nat → Bool)) (hf : Causal f) (n : Nat) (s : Nat → Bool) :
    ∀ i : Nat, i < n → approx f n s i = f s i := by
  intro i hi
  simp only [approx, if_pos hi]
  apply hf
  intro j hj
  exact trunc_agree_le n s i hi j hj

/-- Наближення причинне. -/
theorem approx_causal (f : (Nat → Bool) → (Nat → Bool)) (hf : Causal f) (n : Nat) :
    Causal (approx f n) := by
  intro s t i hst
  simp only [approx]
  split
  · rename_i hi
    apply hf
    intro j hj
    -- trunc n s і trunc n t збігаються на j ≤ i, бо j ≤ i < n
    have hjn : j < n := Nat.lt_of_le_of_lt hj hi
    simp only [trunc, if_pos hjn]
    exact hst j hj
  · rfl

/-- Наближення скінченно визначене на рівні `n`. -/
theorem approx_finDep (f : (Nat → Bool) → (Nat → Bool)) (n : Nat) : FinDep (approx f n) n := by
  intro s t hst
  funext i
  simp only [approx]
  split
  · rename_i hi
    congr 1
    funext j
    simp only [trunc]
    split
    · rename_i hjn
      exact hst j hjn
    · rfl
  · rfl

/-- Твердження 10.10 (модельна форма): щільність скінченно визначених причинних відображень. -/
theorem density (f : (Nat → Bool) → (Nat → Bool)) (hf : Causal f) (n : Nat) :
    ∃ g : (Nat → Bool) → (Nat → Bool), Causal g ∧ FinDep g n ∧
      ∀ s, ∀ i : Nat, i < n → g s i = f s i :=
  ⟨approx f n, approx_causal f hf n, approx_finDep f n, approx_agree f hf n⟩

end SubitDensity
