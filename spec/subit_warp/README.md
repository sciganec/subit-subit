# SUBIT-WARP

**Статус:** DRAFT · NOT STABLE  
**Версія:** v0.4 (W21–W32; канон W23′, RC не оголошено)  
**Дата:** 4 листопада 2026 року  
**Базова система:** SUBIT-∞ v6.13.39 Stable  
**Принцип:** DO NOT COLLAPSE — CONTEXTUALIZE  

---

## Мета

SUBIT-WARP — дослідницький модуль над SUBIT-∞ (підготовка до v6.14), що вивчає взаємозв'язок між:

1. структурою скінченних та нескінченних дерев;
2. простором причинних перетворень;
3. геометрією нескінченних граничних гілок;
4. операторами взаємодії на просторі меж;
5. спектральними властивостями ієрархічних операторів та реконструкцією.

**Дослідницька гіпотеза:** структурна ієрархія Tree∞ індукує геометрію межі, а геометрія межі дозволяє побудувати оператори, спектр яких відображає ієрархічну організацію початкової структури.

WARP не змінює означень базової системи і не є частиною стабільної специфікації.

---

## Архітектурний розподіл (W0–W32)

Модуль розділяє дві фундаментальні системи:

- **STRUCTURAL SYSTEM**: простір адрес, вузли, листки, глибини, відношення батьківства та інваріанти.
- **SPECTRAL SYSTEM**: міри, ядра взаємодії, інтегральні оператори, спектри та операторні збурення.

### Еволюція розділів:
- **W0–W6**: Первинні конструкції (дерева, межа, метрика $d_v$, міра, спадне та обернене ядра).
- **W7–W10**: Спектральний оператор $T_q$, скінченна апроксимація, розмежування параметрів (W9: $\beta = \alpha_w/\alpha_v$, $K_q = d_v^\beta$), верифікація (W10).
- **W11–W20**: Неоднорідні моделі, межі спектральної та структурної реконструкції.
- **W21 / v0.4.0**: Канонічна консолідація (`subit_warp_v0.4.0.md`).
- **W23**: Канонічні виправлення та уніфікована математична специфікація (`subit_warp_v0.4_draft_11_canonical.md`).
- **W24**: Первинний аудит математичних основ W0–W6 (`subit_warp_v0.4_draft_12_audit_2.md`, частковий).
- **W24.16**: Завершений первинний аудит W0–W6 за оригінальним текстом v0.3 (`subit_warp_v0.4_draft_14_audit_3.md`).
- **W23′**: Канонічна редакція W23, виправлена після W24.16: d_F / d_Σ / d_T / d_H, PartialTree як нове розширення, Tω⁺ і теорема W5.4′, K_Vl(ξ,ξ)=0 (`subit_warp_v0.4_draft_13_canonical.md`).
- **W25**: Executable Verification — аналітично й чисельно перевірено; Lean/Rust не виконано (`subit_warp_v0.4_draft_15_audit_4.md`).
- **W26**: Canonical Integration & Release Audit — INTEGRATION CANDIDATE (`subit_warp_v0.4_draft_16_audit_5.md`).
- **W27**: Proof Closure — ANALYTICAL PROOF CLOSURE COMPLETED (`subit_warp_v0.4_draft_17.md`).
- **W28**: Global Consistency & Regression Spec — специфікацію завершено, W20 suite не виконано (`subit_warp_v0.4_draft_18.md`).
- **W29**: Independent Mathematical Audit — **CORRECTIONS REQUIRED** (C-11…C-15) (`subit_warp_v0.4_draft_19.md`).
- **W30**: Theorem Registry & Proof Dependency — MATHEMATICALLY CONSOLIDATED DRAFT (`subit_warp_v0.4_draft_20.md`).
- **W31**: Formalization Boundary & Lean Blueprint — архітектуру задано, реалізації немає (`subit_warp_v0.4_draft_21.md`).
- **W32**: Canonical v0.4 Integration & Release Candidate Audit — Mathematical RC **не оголошено** (`subit_warp_v0.4_draft_22_w32_rc_audit.md`).

**Поточний канон:** `draft_13_canonical` (W23′) залишається заявленим каноном, доки виправлення W29 (C-11…C-15) і застереження W25 (q→1, q⁰=1, ordered/unordered fingerprint) не поглинуті наступною канонічною редакцією (крок I-3 W32). Далі — W33 (RC checklist).

---

## Файли специфікації та аудиту

| Файл | Зміст |
| :-- | :-- |
| [`subit_warp_00_randall_sundrum.md`](subit_warp_00_randall_sundrum.md) | Вихідне есе: аналогія з моделлю Randall–Sundrum |
| [`subit_warp_v0.1.md`](subit_warp_v0.1.md) | Специфікація v0.1 |
| [`subit_warp_v0.2.0.md`](subit_warp_v0.2.0.md) | Специфікація v0.2.0 |
| [`subit_warp_v0.2.1.md`](subit_warp_v0.2.1.md) | Редакція v0.2.1 |
| [`subit_warp_v0.2_audit.md`](subit_warp_v0.2_audit.md) | Аудит v0.2 |
| [`subit_warp_v0.3.md`](subit_warp_v0.3.md) | Специфікація v0.3 (Proof-Refined) |
| [`subit_warp_v0.3_audit_1.md`](subit_warp_v0.3_audit_1.md) | Аудит v0.3: W6–W8 |
| [`subit_warp_v0.3_audit_2.md`](subit_warp_v0.3_audit_2.md) | Аудит v0.3: W9 (перший прохід) |
| [`subit_warp_v0.3_audit_3.md`](subit_warp_v0.3_audit_3.md) | Аудит v0.3: W9 Parameter Separation (фінальний) |
| [`subit_warp_v0.3_audit_4.md`](subit_warp_v0.3_audit_4.md) | Аудит v0.3 (частина 4) |
| [`subit_warp_v0.3_audit_5.md`](subit_warp_v0.3_audit_5.md) | Аудит v0.3 (частина 5) |
| [`subit_warp_v0.4.0.md`](subit_warp_v0.4.0.md) | **v0.4.0: W21 Canonical Specification** |
| [`subit_warp_v0.4_draft_1.md`](subit_warp_v0.4_draft_1.md) – [`_10_audit.md`](subit_warp_v0.4_draft_10_audit.md) | Чернетки та аудити еволюції v0.4 |
| [`subit_warp_v0.4_draft_11_canonical.md`](subit_warp_v0.4_draft_11_canonical.md) | **W23: Canonical Corrections & Unified Specification** |
| [`subit_warp_v0.4_draft_12_audit_2.md`](subit_warp_v0.4_draft_12_audit_2.md) | **W24: Primary Source Audit (W0–W6 foundations)** — частковий, доповнено W24.16 |
| [`subit_warp_v0.4_draft_14_audit_3.md`](subit_warp_v0.4_draft_14_audit_3.md) | **W24.16: Primary Source Audit W0–W6 — COMPLETED WITH CORRECTIONS** (раніше згадувався як `draft_12_audit_3`) |
| [`subit_warp_v0.4_draft_13_canonical.md`](subit_warp_v0.4_draft_13_canonical.md) | **W23′: Canonical Corrections after W24.16 (поточна канонічна редакція)** |
| [`subit_warp_v0.4_draft_15_audit_4.md`](subit_warp_v0.4_draft_15_audit_4.md) | **W25: Executable Verification** |
| [`subit_warp_v0.4_draft_16_audit_5.md`](subit_warp_v0.4_draft_16_audit_5.md) | **W26: Canonical Integration & Release Audit** |
| [`subit_warp_v0.4_draft_17.md`](subit_warp_v0.4_draft_17.md) | **W27: Proof Closure** |
| [`subit_warp_v0.4_draft_18.md`](subit_warp_v0.4_draft_18.md) | **W28: Global Consistency & Regression Spec** |
| [`subit_warp_v0.4_draft_19.md`](subit_warp_v0.4_draft_19.md) | **W29: Independent Mathematical Audit — CORRECTIONS REQUIRED** |
| [`subit_warp_v0.4_draft_20.md`](subit_warp_v0.4_draft_20.md) | **W30: Theorem Registry & Proof Dependency** |
| [`subit_warp_v0.4_draft_21.md`](subit_warp_v0.4_draft_21.md) | **W31: Formalization Boundary & Lean Blueprint** |
| [`subit_warp_v0.4_draft_22_w32_rc_audit.md`](subit_warp_v0.4_draft_22_w32_rc_audit.md) | **W32: Canonical v0.4 Integration & RC Audit** |

---

## Обмеження та статус

- Специфікація має статус **DRAFT · NOT STABLE**; поточний канон — W23′ (`draft_13`); RC не оголошено (W32); наступний крок — I-3, далі W33.
- Lean 4 формалізація та чисельна сертифікація матриць $3^n \times 3^n$ залишаються відкритими (W10).
- Фізична інтерпретація гравітаційних аналогій — суто дослідницька гіпотеза зі статусом `PHYSICAL-CORRESPONDENCE-OPEN`.
