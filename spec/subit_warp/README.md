# SUBIT-WARP

**Статус:** DRAFT · CANONICAL CONSOLIDATION & AUDIT · NOT STABLE  
**Версія:** v0.4 (W21–W24)  
**Дата:** 3 листопада 2026 року  
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

## Архітектурний розподіл (W0–W24)

Модуль розділяє дві фундаментальні системи:

- **STRUCTURAL SYSTEM**: простір адрес, вузли, листки, глибини, відношення батьківства та інваріанти.
- **SPECTRAL SYSTEM**: міри, ядра взаємодії, інтегральні оператори, спектри та операторні збурення.

### Еволюція розділів:
- **W0–W6**: Первинні конструкції (дерева, межа, метрика $d_v$, міра, спадне та обернене ядра).
- **W7–W10**: Спектральний оператор $T_q$, скінченна апроксимація, розмежування параметрів (W9: $\beta = \alpha_w/\alpha_v$, $K_q = d_v^\beta$), верифікація (W10).
- **W11–W20**: Неоднорідні моделі, межі спектральної та структурної реконструкції.
- **W21 / v0.4.0**: Канонічна консолідація (`subit_warp_v0.4.0.md`).
- **W23**: Канонічні виправлення та уніфікована математична специфікація (`subit_warp_v0.4_draft_11_canonical.md`).
- **W24**: Первинний аудит математичних основ W0–W6 (`subit_warp_v0.4_draft_12_audit_2.md`).

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
| [`subit_warp_v0.4_draft_12_audit_2.md`](subit_warp_v0.4_draft_12_audit_2.md) | **W24: Primary Source Audit (W0–W6 foundations)** |

---

## Обмеження та статус

- Специфікація має статус **DRAFT / CANONICAL CONSOLIDATION**.
- Lean 4 формалізація та чисельна сертифікація матриць $3^n \times 3^n$ залишаються відкритими (W10).
- Фізична інтерпретація гравітаційних аналогій — суто дослідницька гіпотеза зі статусом `PHYSICAL-CORRESPONDENCE-OPEN`.
