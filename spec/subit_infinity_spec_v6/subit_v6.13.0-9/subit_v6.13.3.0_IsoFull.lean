/-!
# Твердження 7.8 (Q19): ізоморфізми SUBIT_full — спряження динаміки

Об'єкт X = (S, ℛ, g) з дією `ev : ℛ → S → S` (правило застосоване до стану) і
`g : ℛ × S → ℛ`. Динаміка `D(s, ρ) := (ρ(s), g(ρ, s))`.
Морфізм SUBIT_full: (φ_S, φ_ℛ) з умовами 7.2 і 7.3.
Ізоморфізм: пара морфізмів, композиції — тотожні на кожній компоненті.

Перевіряється: (а) кожен морфізм SUBIT_full, зокрема ізоморфізм, спряжує динаміки;
(б) існують різні g, що дають ізоморфні об'єкти.
Файл використовує лише ядро Lean 4 (без Mathlib).
-/

namespace SubitIso

structure Obj where
  S : Type
  R : Type
  ev : R → S → S
  g : R → S → R

/-- Динаміка на S × ℛ: `D(s, ρ) = (ρ(s), g(ρ, s))`. -/
def Obj.D (X : Obj) (p : X.S × X.R) : X.S × X.R :=
  (X.ev p.2 p.1, X.g p.2 p.1)

/-- Морфізм у SUBIT_full: умови 7.2 (сумісність з оцінкою) і 7.3 (сумісність з g). -/
structure Mor (X Y : Obj) where
  fS : X.S → Y.S
  fR : X.R → Y.R
  comp_ev : ∀ (ρ : X.R) (s : X.S), fS (X.ev ρ s) = Y.ev (fR ρ) (fS s)
  comp_g : ∀ (ρ : X.R) (s : X.S), fR (X.g ρ s) = Y.g (fR ρ) (fS s)

/-- Ізоморфізм: морфізми в обох напрямках, композиції тотожні. -/
structure Iso (X Y : Obj) where
  f : Mor X Y
  h : Mor Y X
  leftS : ∀ s : X.S, h.fS (f.fS s) = s
  leftR : ∀ ρ : X.R, h.fR (f.fR ρ) = ρ
  rightS : ∀ s : Y.S, f.fS (h.fS s) = s
  rightR : ∀ ρ : Y.R, f.fR (h.fR ρ) = ρ

/-- Твердження 7.8(а): морфізм SUBIT_full спряжує динаміки. -/
theorem mor_conj {X Y : Obj} (φ : Mor X Y) (p : X.S × X.R) :
    Y.D (φ.fS p.1, φ.fR p.2) = (φ.fS (X.D p).1, φ.fR (X.D p).2) := by
  obtain ⟨s, ρ⟩ := p
  simp only [Obj.D]
  rw [φ.comp_ev, φ.comp_g]

/-- Твердження 7.8(а) для ізоморфізмів: Φ(s, ρ) := (φ_S s, φ_ℛ ρ) — спряження. -/
theorem iso_conj {X Y : Obj} (ι : Iso X Y) (p : X.S × X.R) :
    Y.D (ι.f.fS p.1, ι.f.fR p.2) = (ι.f.fS (X.D p).1, ι.f.fR (X.D p).2) :=
  mor_conj ι.f p

/-! ### Твердження 7.8(б): різні g дають ізоморфні об'єкти -/

/-- Об'єкт із сталими правилами: правило `r` має значення `r` на всіх станах. -/
def constObj (g : Bool → Bool → Bool) : Obj where
  S := Bool
  R := Bool
  ev := fun r _ => r
  g := g

/-- X: g_X(ρ, s) := true (тобто ρ_a, якщо a = true). -/
def objX : Obj := constObj (fun _ _ => true)

/-- Y: g_Y(ρ, s) := false (тобто ρ_b). -/
def objY : Obj := constObj (fun _ _ => false)

/-- Обмін a ↔ b і ρ_a ↔ ρ_b — це `not` на обох компонентах. -/
def swapMor : Mor objX objY where
  fS := not
  fR := not
  comp_ev := by intro ρ s; rfl
  comp_g := by intro ρ s; rfl

def swapMorBack : Mor objY objX where
  fS := not
  fR := not
  comp_ev := by intro ρ s; rfl
  comp_g := by intro ρ s; rfl

/-- X ≅ Y у SUBIT_full, хоча g_X ≠ g_Y. -/
def isoXY : Iso objX objY where
  f := swapMor
  h := swapMorBack
  leftS := by intro s; cases s <;> rfl
  leftR := by intro ρ; cases ρ <;> rfl
  rightS := by intro s; cases s <;> rfl
  rightR := by intro ρ; cases ρ <;> rfl

/-- Різні g: g_X і g_Y як функції відрізняються. -/
theorem g_differ : objX.g ≠ objY.g := by
  intro h
  have := congrFun (congrFun h true) true
  exact Bool.noConfusion this

end SubitIso
