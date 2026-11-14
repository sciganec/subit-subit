# SUBIT-∞ v6.13.39

Скінченна і нескінченна динаміка над алфавітом A = {T, B, F, N}: специфікація, формальне доведення в Lean 4 і програмна перевірка в Rust.

**Поточний реліз: v6.13.39** — див. [subit_v6.13.39_release_notes.md](subit_v6.13.39_release_notes.md).

## Зміст

| Частина | Файл | Статус |
|---|---|---|
| Специфікація | [`subit_v6.13.39_stable.md`](subit_v6.13.39_stable.md) | Заморожений текст; перевірка часткова |
| Lean 4.32.0 / Mathlib v4.32.0 | [`subit_v6.13.37_lean_mathlib.tar.gz`](subit_v6.13.37_lean_mathlib.tar.gz) | Збирається; без `sorry` (2472 задачі, 0 попереджень) |
| Rust | [`subit_v6.13.31_rust.tar.gz`](subit_v6.13.31_rust.tar.gz) | 57 тестів; тестування, не доведення |
| Журнал рецензування | [`subit_v6.13.39_review.md`](subit_v6.13.39_review.md) | Журнал змін і статусів |
| Відтворюваність | [`subit_v6.13.39_manifest.md`](subit_v6.13.39_manifest.md), [`SHA256SUMS`](SHA256SUMS) | Хеші і логи |

## Статуси

Прапорці статусів тверджень розшифровано в §0.1 специфікації та в `subit_v6.13.39_review.md`. Коротко:

- **LEAN-CHECKED** — частково: твердження з Додатку Е, а також свідки W6–W8 (W6 у v6.13.36, W7 у v6.13.37, W8 у v6.13.28).
- **RUST-TESTED** — частково: 57 тестів на станах специфікації і малих системах, Pilot-01.
- **BUILD-PASSED-FROM-ARCHIVE** — 🟡 ЧАСТКОВО: чиста збірка `lake build Subit` з архіву з кешем Mathlib (`lake exe cache get`) незалежно відтворена (2472 задачі, 0 попереджень).
- **Людського рецензента немає.** Перевірка виконувалася лише мультиагентною перехресною перевіркою.

## Швидкий перегляд

Lean:

```bash
tar xzf subit_v6.13.37_lean_mathlib.tar.gz
cd pm
lake build Subit
```

Очікуваний результат: 2472 задачі, 0 попереджень (lean-toolchain: `leanprover/lean4:v4.32.0`).

Аксіоми W7:

```bash
lake env lean checks/w7_release_axioms_v6.13.37.lean
```

Очікуваний результат — лише `propext`, `Classical.choice`, `Quot.sound` (див. `w7_release_axioms_v6.13.37.log`).

Rust:

```bash
tar xzf subit_v6.13.31_rust.tar.gz
cd subit
cargo test          # 57 тестів
cargo clippy --all-targets
cargo run --release --bin pilot01
```

Перевірка цілісності файлів:

```bash
sha256sum -c SHA256SUMS
```

## Відомі обмеження

- Повне відтворення самого Mathlib з нуля в проєкті не виконувалося; перевірено рівень `Subit` з кешем.
- Відкриті питання: Q10′ (MIN × NONATTAINED), A4 для n > 64^63, Lemma 11.9 поза Tree∞ і S∞ × ℛ₀.
