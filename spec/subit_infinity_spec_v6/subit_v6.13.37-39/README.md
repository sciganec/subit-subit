# SUBIT-∞ v6.13.37–v6.13.39

Поточний стабільний реліз. Три мікрорелізи: Lean-верифікація W7 (v6.13.37) + текстові правки статусів (v6.13.38–39).

---

## Файли

| Файл | Призначення |
| :-- | :-- |
| [`subit_v6.13.39_stable.md`](subit_v6.13.39_stable.md) | Специфікація (заморожений текст, поточна версія) |
| [`subit_v6.13.38_stable.md`](subit_v6.13.38_stable.md) | Попередня текстова редакція |
| [`subit_v6.13.37_stable.md`](subit_v6.13.37_stable.md) | Перший реліз цього пакету |
| [`subit_v6.13.37_lean_mathlib.tar.gz`](subit_v6.13.37_lean_mathlib.tar.gz) | Lean 4.32.0 / Mathlib v4.32.0 |
| [`subit_v6.13.39_manifest.md`](subit_v6.13.39_manifest.md) | SHA-256 і відтворюваність (поточний) |
| [`subit_v6.13.38_manifest.md`](subit_v6.13.38_manifest.md) | SHA-256 (v6.13.38) |
| [`subit_v6.13.37_manifest.md`](subit_v6.13.37_manifest.md) | SHA-256 (v6.13.37) |
| [`subit_v6.13.39_release_notes.md`](subit_v6.13.39_release_notes.md) | Що змінено у v6.13.39 |
| [`subit_v6.13.38_release_notes.md`](subit_v6.13.38_release_notes.md) | Що змінено у v6.13.38 |
| [`subit_v6.13.37_release_notes.md`](subit_v6.13.37_release_notes.md) | Що змінено у v6.13.37 |
| [`subit_v6.13.39_review.md`](subit_v6.13.39_review.md) | Журнал рецензування |
| [`subit_v6.13.38_review.md`](subit_v6.13.38_review.md) | Журнал рецензування |
| [`subit_v6.13.37_review.md`](subit_v6.13.37_review.md) | Журнал рецензування |
| [`subit_v6.13.39_playground.html`](subit_v6.13.39_playground.html) | Інтерактивний перегляд |

---

## Lean

```bash
tar xzf subit_v6.13.37_lean_mathlib.tar.gz
cd pm
lake build Subit
```

Очікується: **2472 задачі, 0 попереджень** (`leanprover/lean4:v4.32.0`).

Перевірка аксіом W7:

```bash
lake env lean checks/w7_release_axioms_v6.13.37.lean
```

Очікується: лише `propext`, `Classical.choice`, `Quot.sound`.

Перевірка цілісності файлів:

```bash
sha256sum -c SHA256SUMS
```

---

## Що перевірено Lean

| Модуль | Свідок | Зміст |
| :-- | :-- | :-- |
| `W6Word.lean`, `W6Tree.lean` | W6 | Interaction Kernels |
| `W7Abstract.lean`, `W7Word.lean`, `W7Tree.lean` | W7 | Spectral Operator (NONMIN_POS × NONATTAINED) |
| `W8GTree.lean` | W8 | NONMIN_ZERO × ATTAINED |
| Додаток Е | — | Перелік усіх Lean-теорем |

---

## Хронологія релізів

**v6.13.37** (Lean-реліз):
- Нові модулі W7: `W7Abstract`, `W7Word`, `W7Tree`.
- Статус W7: DP-f → LEAN-CHECKED.
- 2472 задачі, 0 попереджень, 0 помилок.

**v6.13.38** (текстові правки):
- Реєстр Дод. Д: T6/T9 розділено; W5 з посиланням на §11.10.
- §0.1: LEAN-CHECKED доповнено W6 і W7.

**v6.13.39** (текстові правки):
- Дод. Е: таблиця W6/W7-теорем (25 Lean-теорем верифіковано пошуком).
- §0.2: «свідки W1–W5» → «W1–W8».
- §11.6 W7: T := t∘σ∘t⁻¹ сюр'єктивне (явно).
- §11.6 W8, Дод. В, реєстр: «LEAN-CHECKED (v6.13.28, `W8GTree.lean`)».

Lean-код і Rust-код не змінювались між v6.13.37 і v6.13.39.

---

## Відомі обмеження

- Повне відтворення з нуля разом із Mathlib не виконувалось.
- Людського рецензента немає; перевірка — мультиагентна перехресна.
- Відкриті: Q10′ (MIN × NONATTAINED), A4 для n > 64^63, Lemma 11.9 поза Tree∞ і S∞ × ℛ₀.
- Статус d_ω у §10.10 («DP-f за уточненням 10.2») відкрито для рішення.
