import Subit.DSExact

/-!
# Твердження 10.10 (Q25-new) на Tree∞

Для нерозтягувального `F : Tree∞ → Tree∞` (ℛ₀ за d_S) і `n` існує нерозтягувальне `G`,
скінченно визначене на рівні `n` і таке, що `d_S(G s, F s) ≤ 2^{-n}`.

Конструкція: `tr a₀ n f` зберігає мітки на довжинах `< n`; на довжині `n` вузол або листок
стає листком `a₀`, `none` лишається `none`; на довжинах `> n` — `none`.
`G(s) := tr(F(tr s))`.
-/

namespace Subit
open Set

variable {A : Type*}

/-- Обрізання дерева на рівні `n` із листком `a₀` на межі. -/
def tr (a₀ : A) (n : ℕ) (f : Pos → Lab A) : Pos → Lab A :=
  fun σ =>
    if σ.length < n then f σ
    else if σ.length = n then (match f σ with | .none => .none | _ => .leaf a₀)
    else .none

theorem tr_lt (a₀ : A) (n : ℕ) (f : Pos → Lab A) {σ : Pos} (h : σ.length < n) :
    tr a₀ n f σ = f σ := by
  simp [tr, h]

theorem tr_eq (a₀ : A) (n : ℕ) (f : Pos → Lab A) {σ : Pos} (h : σ.length = n) :
    tr a₀ n f σ = (match f σ with | .none => .none | _ => .leaf a₀) := by
  simp [tr, h]

theorem tr_gt (a₀ : A) (n : ℕ) (f : Pos → Lab A) {σ : Pos} (h : n < σ.length) :
    tr a₀ n f σ = .none := by
  simp [tr, Nat.not_lt.mpr h.le, Nat.ne_of_gt h]

theorem tr_isTree (a₀ : A) (n : ℕ) {f : Pos → Lab A} (hf : IsTree f) :
    IsTree (tr a₀ n f) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · -- (T1)
    by_cases hn : 0 < n
    · rw [tr_lt a₀ n f (by simpa using hn)]
      exact hf.t1
    · have h0 : n = 0 := by omega
      subst h0
      rw [tr_eq a₀ 0 f (by simp)]
      have h1 : f [] ≠ .none := hf.t1
      generalize f [] = x at h1 ⊢
      cases x <;> simp_all
  · -- (T2)
    intro σ hσ i
    have hlt : σ.length < n := by
      rcases Nat.lt_trichotomy σ.length n with h | h | h
      · exact h
      · rw [tr_eq a₀ n f h] at hσ
        cases hfσ : f σ <;> simp_all
      · rw [tr_gt a₀ n f h] at hσ
        cases hσ
    rw [tr_lt a₀ n f hlt] at hσ
    have hfσ : f σ = .node := hσ
    have hc := hf.t2 σ hfσ i
    have hlen : (σ ++ [i]).length = σ.length + 1 := by simp
    rcases Nat.lt_trichotomy (σ ++ [i]).length n with hc' | hc' | hc'
    · rw [tr_lt a₀ n f hc']
      exact hc
    · rw [tr_eq a₀ n f hc']
      cases hfc : f (σ ++ [i]) <;> simp_all
    · exfalso
      omega
  · -- (T3)
    intro σ a hσ i
    have hle : σ.length ≤ n := by
      rcases Nat.lt_or_ge n σ.length with h | h
      · rw [tr_gt a₀ n f h] at hσ
        cases hσ
      · exact h
    rcases Nat.lt_or_ge σ.length n with hlt | hge
    · rw [tr_lt a₀ n f hlt] at hσ
      have hfc := hf.t3 σ a hσ i
      have hlen : (σ ++ [i]).length = σ.length + 1 := by simp
      rcases Nat.lt_trichotomy (σ ++ [i]).length n with hc' | hc' | hc'
      · rw [tr_lt a₀ n f hc']
        exact hfc
      · rw [tr_eq a₀ n f hc', hfc]
      · exfalso
        omega
    · have heq : σ.length = n := le_antisymm hle hge
      have hgt : n < (σ ++ [i]).length := by simp; omega
      exact tr_gt a₀ n f hgt
  · -- (T4)
    intro σ hσ τ
    have hL : (σ ++ τ).length = σ.length + τ.length := by simp
    rcases Nat.lt_or_ge n (σ ++ τ).length with hg | hle
    · exact tr_gt a₀ n f hg
    · have hσle : σ.length ≤ n := by omega
      have hfσ : f σ = .none := by
        rcases Nat.lt_or_ge σ.length n with h | h
        · rw [tr_lt a₀ n f h] at hσ
          exact hσ
        · have heq : σ.length = n := le_antisymm hσle h
          rw [tr_eq a₀ n f heq] at hσ
          cases hfσ' : f σ <;> simp_all
      have hfστ := hf.t4 σ hfσ τ
      rcases Nat.lt_trichotomy (σ ++ τ).length n with h | h | h
      · rw [tr_lt a₀ n f h]
        exact hfστ
      · simp [tr_eq a₀ n f h, hfστ]
      · omega


/-- Агрегований варіант: розбіжностей з довжиною `< n` немає ⇒ `d_S ≤ 2^{-n}`. -/
theorem dS_le_of_agree (f g : Pos → Lab A) (n : ℕ)
    (h : ∀ σ : Pos, σ.length < n → f σ = g σ) : dS f g ≤ (1 / 2 : ℝ) ^ n := by
  unfold dS
  apply Real.iSup_le _ (by positivity)
  rintro ⟨σ, hσ⟩
  have hn : n ≤ σ.length := by
    by_contra hc
    exact hσ (h σ (not_le.mp hc))
  exact pow_le_pow_of_le_one (by norm_num) (by norm_num) hn

theorem dS_self' (x : Pos → Lab A) : dS x x = 0 := (dS_eq_zero_iff x x).2 rfl

/-- Нерозтягування в термінах `d_S` на Tree∞ (ℛ₀). -/
def TNonexp (F : Tree A → Tree A) : Prop :=
  ∀ s t : Tree A, dS (F s).1 (F t).1 ≤ dS s.1 t.1

/-- Обрізання на рівні `n` як відображення Tree∞ → Tree∞. -/
def trT (a₀ : A) (n : ℕ) (s : Tree A) : Tree A :=
  ⟨tr a₀ n s.1, tr_isTree a₀ n s.2⟩

/-- Наближення `G(s) := tr(F(tr s))`. -/
def Gap (a₀ : A) (n : ℕ) (F : Tree A → Tree A) (s : Tree A) : Tree A :=
  trT a₀ n (F (trT a₀ n s))

theorem trT_agree_lt (a₀ : A) (n : ℕ) (s : Tree A) {σ : Pos} (h : σ.length < n) :
    (trT a₀ n s).1 σ = s.1 σ :=
  tr_lt a₀ n s.1 h

theorem trT_eq_of_agree (a₀ : A) (n : ℕ) (s t : Tree A)
    (h : ∀ σ : Pos, σ.length ≤ n → s.1 σ = t.1 σ) : trT a₀ n s = trT a₀ n t := by
  apply Subtype.ext
  funext σ
  show tr a₀ n s.1 σ = tr a₀ n t.1 σ
  rcases Nat.lt_or_ge n σ.length with hg | hle
  · rw [tr_gt a₀ n s.1 hg, tr_gt a₀ n t.1 hg]
  · rcases Nat.lt_trichotomy σ.length n with h1 | h1 | h1
    · rw [tr_lt a₀ n s.1 h1, tr_lt a₀ n t.1 h1]
      exact h σ hle
    · rw [tr_eq a₀ n s.1 h1, tr_eq a₀ n t.1 h1, h σ hle]
    · omega

/-- Скінченна визначеність: `G` залежить лише від міток на довжинах `≤ n`. -/
theorem Gap_finDep (a₀ : A) (n : ℕ) (F : Tree A → Tree A) (s t : Tree A)
    (h : ∀ σ : Pos, σ.length ≤ n → s.1 σ = t.1 σ) : Gap a₀ n F s = Gap a₀ n F t := by
  unfold Gap
  rw [trT_eq_of_agree a₀ n s t h]

/-- Оцінка `d_S(G s, F s) ≤ 2^{-n}`. -/
theorem Gap_close (a₀ : A) (n : ℕ) (F : Tree A → Tree A) (hF : TNonexp F) (s : Tree A) :
    dS (Gap a₀ n F s).1 (F s).1 ≤ (1 / 2 : ℝ) ^ n := by
  have h1 : dS (Gap a₀ n F s).1 (F (trT a₀ n s)).1 ≤ (1 / 2 : ℝ) ^ n := by
    apply dS_le_of_agree _ _ n
    intro σ hσ
    unfold Gap
    show (trT a₀ n (F (trT a₀ n s))).1 σ = (F (trT a₀ n s)).1 σ
    exact trT_agree_lt a₀ n _ hσ
  have h2 : dS (F (trT a₀ n s)).1 (F s).1 ≤ (1 / 2 : ℝ) ^ n := by
    refine le_trans (hF (trT a₀ n s) s) ?_
    apply dS_le_of_agree _ _ n
    intro σ hσ
    exact trT_agree_lt a₀ n s hσ
  exact le_trans (dS_ultra _ (F (trT a₀ n s)).1 _) (max_le h1 h2)

/-- Нерозтягування `G`. -/
theorem Gap_nonexp (a₀ : A) (n : ℕ) (F : Tree A → Tree A) (hF : TNonexp F) :
    TNonexp (Gap a₀ n F) := by
  intro s t
  by_cases hst : s.1 = t.1
  · have hs : s = t := Subtype.ext hst
    subst hs
    simp only [dS_self', le_refl]
  · obtain ⟨m, hm, _, hmin⟩ := dS_eq_pow_minlen s.1 t.1 hst
    rw [hm]
    by_cases hmn : m ≤ n
    · have hUV : dS (trT a₀ n s).1 (trT a₀ n t).1 ≤ (1 / 2 : ℝ) ^ m := by
        apply dS_le_of_agree _ _ m
        intro σ hσ
        rw [trT_agree_lt a₀ n s (by omega), trT_agree_lt a₀ n t (by omega)]
        by_contra hne
        have := hmin σ hne
        omega
      have hFUV : dS (F (trT a₀ n s)).1 (F (trT a₀ n t)).1 ≤ (1 / 2 : ℝ) ^ m :=
        le_trans (hF _ _) hUV
      have hagreeF : ∀ σ : Pos, σ.length < m →
          (F (trT a₀ n s)).1 σ = (F (trT a₀ n t)).1 σ := by
        intro σ hσ
        by_contra hne
        have h1 := le_dS hne
        have h2 : (1 / 2 : ℝ) ^ m < (1 / 2 : ℝ) ^ σ.length :=
          pow_lt_pow_right_of_lt_one₀ (by norm_num) (by norm_num) hσ
        linarith
      apply dS_le_of_agree _ _ m
      intro σ hσ
      unfold Gap
      show (trT a₀ n (F (trT a₀ n s))).1 σ = (trT a₀ n (F (trT a₀ n t))).1 σ
      rw [trT_agree_lt a₀ n _ (by omega), trT_agree_lt a₀ n _ (by omega)]
      exact hagreeF σ hσ
    · have hagree : ∀ σ : Pos, σ.length ≤ n → s.1 σ = t.1 σ := by
        intro σ hσ
        by_contra hne
        have := hmin σ hne
        omega
      have hG : Gap a₀ n F s = Gap a₀ n F t := Gap_finDep a₀ n F s t hagree
      rw [hG, dS_self']
      positivity

/-- Твердження 10.10 на Tree∞ (модельна форма ℛ₀ → ℛ_comp, без опису правил). -/
theorem density_tree (a₀ : A) (F : Tree A → Tree A) (hF : TNonexp F) (n : ℕ) :
    ∃ G : Tree A → Tree A, TNonexp G ∧
      (∀ s t : Tree A, (∀ σ : Pos, σ.length ≤ n → s.1 σ = t.1 σ) → G s = G t) ∧
      ∀ s : Tree A, dS (G s).1 (F s).1 ≤ (1 / 2 : ℝ) ^ n :=
  ⟨Gap a₀ n F, Gap_nonexp a₀ n F hF, fun s t h => Gap_finDep a₀ n F s t h,
    Gap_close a₀ n F hF⟩

end Subit
