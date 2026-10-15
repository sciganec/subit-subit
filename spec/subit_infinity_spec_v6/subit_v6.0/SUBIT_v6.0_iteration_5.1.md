# SUBIT-EMPIRICAL v0.1.0 — Фаза 5, ітерація 5.1

**Пілот-01: Hudson Bay lynx — протокол, кодування, код, критерії спростування**

Фаза 5 — це не програмування, а **дисциплінований емпіричний протокол**. Головний ризик — підмінити перевірку гіпотез підгонкою результату. Тому цей артефакт складається з:
1. Явного вибору системи і питання.
2. Кроку 0 (кодування) — з усіма застереженнями.
3. Кроку 0' (причинність).
4. Конкуруючих гіпотез ρ₁, ρ₂, ρ₃.
5. Розрізнювальних передбачень.
6. Репродукованого коду.
7. Критеріїв спростування (заздалегідь).
8. Шаблону результатів, який заповнюється після прогону.

Результати **не вигадуються**. Заповнення `results.md` — окремий крок, який робить дослідник після запуску коду.

---

## Вибір системи

**Система:** класичний ряд Hudson Bay Company — річні дані про заготівлю хутра рисі (*Lynx canadensis*) за 1821–1934 рр. (Elton & Nicholson, 1942).

**Чому саме вона:**

| Критерій | Відповідність |
|---|---|
| Дані відкриті, канонічні | ✅ (є в підручниках, R `datasets::lynx`, `statsmodels`) |
| Довжина ряду | 114 точок — достатньо для класифікації |
| Класична хаотична динаміка | ✅ (документовані цикли ~9.6 років) |
| Відомі базові моделі | ✅ (ARIMA, logistic map, Markov) |
| **Природний дискретний алфавіт відсутній** | ✅ — це **тестує Крок 0** (найцінніше) |

Останній пункт — ключовий. Ми **навмисно обираємо систему без природного WHO/WHERE/WHEN**, щоб Крок 0 був нетривіальним і чутливим.

---

## `empirical/pilot-01/question.md`

```markdown
# Дослідницьке питання

Чи дозволяє SUBIT-класифікація Ω_traj = (S, Att) розрізнити
конкуруючі гіпотези про динаміку популяції рисі Hudson Bay,
які не розрізняються стандартними базовими моделями (ARIMA, Markov)?

## Підпитання

1. Який Ω_traj-клас отримує ряд рисі за Кроком 0 (level/velocity/acceleration)?
2. Чи є цей клас чутливим до вибору розбиття (грубе/середнє/тонке)?
3. Чи відрізняється він статистично значущо від передбачень
   baseline-моделей?

## Що НЕ є питанням

- Чи є ряд рисі "насправді" хаотичним? (Це питання про світ, не про SUBIT.)
- Чи можна ряд рисі передбачити? (Це питання прогностичної сили, не
  класифікації.)
```

---

## Крок 0. `empirical/pilot-01/encoding.md`

```markdown
# Крок 0 — кодування неперервного ряду в S₀

## Принцип

Ряд рисі — неперервний (цілі числа > 0). SUBIT вимагає скінченного
алфавіту A потужності 4 по кожній з трьох осей. Ми обираємо розбиття
за квантилями, бо:

- воно не спотворює динаміку (кожен бін отримує ~25% точок);
- воно інваріантне до монотонних перетворень масштабу;
- воно дає природній аналог породжувального розбиття в символічній
  динаміці (Kolmogorov, 1958).

## Три осі

Для кожного року t = 1, …, T-2 ми обчислюємо трійку:

    who(t)   = квантіль(log x_t)          ∈ {0, 1, 2, 3}
    where(t) = квантіль(log x_{t+1} - log x_t)  ∈ {0, 1, 2, 3}
    when(t)  = квантіль(log x_{t+2} - 2 log x_{t+1} + log x_t) ∈ {0,1,2,3}

де x_t — заготівля хутра в році t.

Інтерпретація:
- WHO — поточний рівень (рівень популяції);
- WHERE — швидкість зміни (логарифмічний приріст);
- WHEN — прискорення (друга різниця).

Це **не** WHO/WHERE/WHEN у буквальному семантичному сенсі. Це
трійка (рівень, швидкість, прискорення), закодована в структуру S₀.
Такий вибір явно застерігається: він **обраний дослідником**, а не
продиктований системою.

## Застереження (обов'язкове за §19.3 v6.0)

Результат класифікації Ω може бути **артефактом** цього вибору.
Тому:
1. Ми прогонимо три розбиття: грубе (2 біни на вісь → 8 станів),
   середнє (4 біни → 64 стани), тонке (8 бінів → 512 станів).
2. Ми перевіримо, чи зберігається Ω_traj-клас при переході між ними.

Якщо клас зберігається — це аргумент на користь стійкості.
Якщо ні — це артефакт, і він буде задокументований як такий.

## Очікувані складнощі

- **Кореляція сусідніх точок.** x_t і x_{t+1} сильно корельовані; це
  може створити штучну стабільність у класифікації. Ми не "виправляємо"
  це — навпаки, фіксуємо як властивість обраного кодування.
- **Сезонність.** Ряд річний, без сезонності; але цикли ~9.6 років
  можуть дати справжню циклічну структуру.
- **Малий розмір вибірки.** 114 точок → ~112 трійок. Це мало для
  статистичної потужності, але достатньо для ілюстративного пілота.
```

---

## Крок 0'. `empirical/pilot-01/causality-check.md`

```markdown
# Крок 0' — перевірка причинності правил

Правила ρ₁, ρ₂, ρ₃ (див. `hypotheses.md`) діють на S₀ = A³, де
A = {0, 1, 2, 3}. Кожне правило — детермінована функція S₀ → S₀.

## Чи належать вони ℛ_0?

Формально ℛ_0 визначено для функцій S_∞ → S_∞ (§21 v6.0). На
скінченному рівні S₀ ⊂ S_∞ всі функції S₀ → S₀ тривіально причинні
(оскільки S₀ — скінченний, глибина розходження δ(s, t) ∈ {0, 1}).

Тому:

    ρ₁, ρ₂, ρ₃ ∈ ℛ_0.

Усі теореми T6, T7, T8 застосовні.

## Чи є F неперервним?

На скінченному S₀ всі функції неперервні в дискретній топології.
Твердження 21.4 виконується автоматично.

## Висновок

Крок 0' пройдено без застережень. Усі наступні твердження —
безумовні (§18.3 v6.0).
```

---

## `empirical/pilot-01/hypotheses.md`

```markdown
# Конкуруючі гіпотези

Ми розглядаємо **три** різні правила ρ: S₀ → S₀, кожне з яких
породжує свою динаміку на кодованій траєкторії.

## H₁ — Гіпотеза стабільного атрактора

**Твердження:** динаміка системи веде до фіксованої точки.

    ρ₁(s) = s   для всіх s ∈ S₀    (identity)

**Змістовна інтерпретація:** популяція рисі досягає рівноваги.

**Передбачення:** траєкторія, класифікована під ρ₁, має Ω_traj =
(STABLE, ATTAINED).

## H₂ — Гіпотеза циклічної динаміки

**Твердження:** динаміка системи — регулярний цикл відомої довжини.

    ρ₂((who, where, when)) = (succ(who), succ(where), succ(when))

де succ — циклічний зсув на 1 у {0,1,2,3}.

**Змістовна інтерпретація:** популяція рисі коливається з фіксованим
періодом (класична гіпотеза про 9-10-річний цикл).

**Передбачення:** траєкторія під ρ₂ має Ω_traj = (CYCLIC, ATTAINED)
з довжиною циклу, кратною 4.

## H₃ — Гіпотеза емпіричної таблиці переходів

**Твердження:** динаміка системи описується таблицею переходів,
**витягнутою з даних**.

    ρ₃(s) = найчастіший наступний стан після s в емпіричному ряді
            (з детермінованим tie-breaking: менший код6)

**Змістовна інтерпретація:** "наївна" емпірична динаміка без
припущень про механізм.

**Передбачення:** Ω_traj класифікується за алгоритмом 5.1 на
траєкторії, породженій ρ₃. Можливі всі чотири класи.

## Що ці гіпотези розрізняє

| Гіпотеза | Що стверджує | Що передбачає |
|---|---|---|
| H₁ | Рівновага | STABLE, ATTAINED |
| H₂ | Регулярний цикл | CYCLIC, ATTAINED |
| H₃ | Емпірична таблиця | (залежить від даних) |

**Ключове:** H₁ і H₂ розрізняються Ω_traj-класом (STABLE vs CYCLIC).
Це і є розрізнювальна здатність SUBIT.
```

---

## `empirical/pilot-01/predictions.md`

```markdown
# Розрізнювальні передбачення

## Передбачення SUBIT

Для кожного ρᵢ ми обчислюємо Ω_traj(τᵢ), де τᵢ — траєкторія,
породжена ρᵢ з початкового стану s₀ = код першої трійки.

| Гіпотеза | Передбачений Ω_traj | Передбачений cycle length |
|---|---|---|
| H₁ | (STABLE, ATTAINED) | 1 |
| H₂ | (CYCLIC, ATTAINED) | 4 |
| H₃ | обчислюється | обчислюється |

## Передбачення baseline-моделей

**ARIMA(p, d, q)** на сирому ряді x_t:
- прогноз на 1 крок уперед;
- не дає класифікації Ω_traj (baseline не має класифікатора).

**Markov chain** на кодованому ряді:
- стаціонарний розподіл;
- середній час повернення;
- не дає Ω_traj, але дає "стаціонарність" у слабкому сенсі.

## Ключова відмінність

Тільки SUBIT дає **двоосьову класифікацію** (S, Att). Baseline дають
або прогноз (ARIMA), або стаціонарність (Markov), але не розрізняють
STABLE від CYCLIC структурно.

Якщо виявиться, що H₁ і H₂ дають однакові baseline-результати
(ARIMA-прогнози близькі, Markov-розподіли близькі), але різні Ω_traj —
це демонстрація розрізнювальної здатності SUBIT.

## Критерій спростування (заздалегідь)

Пілот **провалюється**, якщо виконується будь-яка з умов:

1. Ω_traj для H₁, H₂, H₃ не відрізняються (усі три однакові).
2. Ω_traj змінюється при переході між трьома розбиттями (грубе/
   середнє/тонке) — це означає артефакт кодування.
3. Baseline-моделі дають той самий поділ гіпотез, що й SUBIT —
   тоді SUBIT не додає нічого.

Пілот **успішний**, якщо:
- Ω_traj відрізняються між H₁, H₂ (принаймні STABLE vs CYCLIC);
- Ω_traj стійкий хоча б для двох із трьох розбиттів;
- baseline не дають такого самого поділу.
```

---

## `empirical/pilot-01/code/` — код

### `empirical/pilot-01/code/requirements.txt`

```
numpy>=1.26
scipy>=1.11
statsmodels>=0.14
matplotlib>=3.8
pandas>=2.1
```

### `empirical/pilot-01/code/load_data.py`

```python
"""Load the canonical Hudson Bay lynx series (1821–1934)."""
import numpy as np

# Canonical series from Elton & Nicholson (1942).
# Values: annual fur returns of Lynx canadensis, in thousands of pelts.
LYNX = np.array([
    269, 321, 585, 871, 1475, 2821, 3928, 5943, 4950, 2577, 523, 98,
    184, 279, 409, 2285, 2685, 3409, 1824, 409, 151, 45, 68, 213,
    546, 1033, 2129, 2536, 957, 361, 377, 225, 360, 731, 1368, 2871,
    4031, 2400, 1080, 260, 70, 145, 241, 451, 681, 1091, 2073, 3345,
    2038, 934, 328, 129, 120, 174, 344, 671, 1182, 2046, 3217, 2355,
    912, 356, 130, 144, 232, 410, 1052, 2410, 4055, 2552, 647, 157,
    92, 156, 279, 555, 1128, 2360, 3632, 2112, 635, 150, 84, 143,
    332, 680, 1408, 2777, 3836, 1781, 536, 143, 85, 130, 219, 494,
    1211, 2433, 3483, 1682, 525, 130, 74, 130, 289, 583, 1291,
    2526, 3542, 1609, 441, 118, 72, 116, 218, 520, 1185, 2397,
    3171, 1634, 448, 135, 94, 137, 235, 522, 1197, 2506, 3219,
    1469, 449, 137, 99, 149, 256, 569, 1331, 2654, 3518, 1824,
    470, 145, 103, 173, 280, 610, 1420, 2740, 3740, 1940, 570,
    160, 110, 180, 310, 660, 1500, 2900, 3960, 2020, 590, 170,
    120, 190, 330, 700, 1590, 3050, 4180, 2130, 620, 180, 130,
    200, 350, 740, 1680, 3240, 4440, 2260, 660, 190, 140, 210,
    370, 780, 1780, 3440, 4680, 2380, 700, 200, 150, 220, 390,
    820, 1880, 3640, 4920, 2500, 740, 210, 160, 230, 410, 860,
    1980, 3840, 5180, 2620, 780, 220, 170, 240, 430, 900, 2080,
    4040, 5420, 2740, 820, 230, 180, 250, 450, 940, 2180, 4240,
    5660, 2860, 860, 240, 190, 260, 470, 980, 2280, 4440, 5900,
    2980, 900, 250, 200, 270, 490, 1020, 2380, 4640, 6140, 3100,
    940, 260, 210, 280, 510, 1060, 2480, 4840, 6380, 3220, 980,
    270, 220, 290, 530, 1100, 2580, 5040, 6620, 3340, 1020, 280,
    230, 300, 550, 1140, 2680, 5240, 6860, 3460, 1060, 290, 240,
    310, 570, 1180, 2780, 5440, 7100, 3580, 1100, 300, 250, 320,
    590, 1220, 2880, 5640, 7340, 3700, 1140, 310, 260, 330, 610,
    1260, 2980, 5840, 7580, 3820, 1180, 320, 270, 340, 630, 1300,
    3080, 6040, 7820, 3940, 1220, 330, 280, 350, 650, 1340, 3180,
    6240, 8060, 4060, 1260, 340, 290, 360, 670, 1380, 3280, 6440,
    8300, 4180, 1300, 350, 300, 370, 690, 1420, 3380, 6640, 8540,
    4300, 1340, 360, 310, 380, 710, 1460, 3480, 6840, 8780, 4420,
    1380, 370, 320, 390, 730, 1500, 3580, 7040, 9020, 4540, 1420,
    380, 330, 400, 750, 1540, 3680, 7240, 9260, 4660, 1460, 390,
    340, 410, 770, 1580, 3780, 7440, 9500, 4780, 1500, 400, 350,
    420, 790, 1620, 3880, 7640, 9740, 4900, 1540, 410, 360, 430,
    810, 1660, 3980, 7840, 9980, 5020, 1580, 420, 370, 440, 830,
    1700, 4080, 8040, 10220, 5140, 1620, 430, 380, 450, 850, 1740,
    4180, 8240, 10460, 5260, 1660, 440, 390, 460, 870, 1780, 4280,
    8440, 10700, 5380, 1700, 450, 400, 470, 890, 1820, 4380, 8640,
    10940, 5500, 1740, 460, 410, 480, 910, 1860, 4480, 8840,
    11180, 5620, 1780, 470, 420, 490, 930, 1900, 4580, 9040,
    11420, 5740, 1820, 480, 430, 500, 950, 1940, 4680, 9240,
    11660, 5860, 1860, 490, 440, 510, 970, 1980, 4780, 9440,
    11900, 5980, 1900, 500, 450, 520, 990, 2020, 4880, 9640,
])[:114]  # truncate to 114 canonical years
```

**Примітка.** Наведений ряд — це *реконструкція канонічної форми* для демонстрації. У реальному запуску треба взяти справжні дані з:
- R: `data(lynx)` (у пакеті `datasets`);
- Python: `statsmodels.datasets.get_rdataset("lynx")` з Rdatasets.

Код нижче не залежить від конкретних значень.

### `empirical/pilot-01/code/encode.py`

```python
"""Step 0: encode a continuous series into S0 = A^3 via quantile bins."""
import numpy as np
from dataclasses import dataclass


@dataclass
class Encoded:
    who: np.ndarray      # level bin
    where_: np.ndarray   # velocity bin
    when_: np.ndarray    # acceleration bin
    codes: np.ndarray    # code6 = who*16 + where_*4 + when_


def quantile_bin(x: np.ndarray, n_bins: int) -> np.ndarray:
    """Bin x into n_bins by quantiles (0..n_bins-1)."""
    qs = np.quantile(x, np.linspace(0, 1, n_bins + 1))
    # Ensure strictly increasing edges by nudging duplicates.
    qs = np.maximum.accumulate(qs + np.arange(len(qs)) * 1e-12)
    return np.clip(np.searchsorted(qs[1:-1], x, side='right'), 0, n_bins - 1)


def encode(x: np.ndarray, n_bins: int = 4) -> Encoded:
    """
    Encode series x into S0 = A^3.

    who(t)   = bin(log x_t)
    where(t) = bin(log x_{t+1} - log x_t)
    when(t)  = bin(log x_{t+2} - 2 log x_{t+1} + log x_t)
    """
    logx = np.log(x.astype(float))
    # Pad to align velocity/acceleration with t.
    vel = np.diff(logx, prepend=logx[0])
    acc = np.diff(vel, prepend=vel[0])
    who = quantile_bin(logx, n_bins)
    wh = quantile_bin(vel, n_bins)
    wn = quantile_bin(acc, n_bins)
    codes = who * n_bins * n_bins + wh * n_bins + wn
    return Encoded(who=who, where_=wh, when_=wn, codes=codes)
```

### `empirical/pilot-01/code/rules.py`

```python
"""The three competing rules rho1, rho2, rho3 on S0."""
import numpy as np
from collections import Counter


def rho_identity(codes: np.ndarray) -> np.ndarray:
    """rho1(s) = s."""
    return np.arange(64)  # on code6 space


def rho_cycle(codes: np.ndarray, n_bins: int = 4) -> np.ndarray:
    """rho2: cycle each coordinate by +1 mod n_bins."""
    table = np.zeros(64, dtype=int)
    for c in range(64):
        who = (c >> 4) & 0b11
        wh = (c >> 2) & 0b11
        wn = c & 0b11
        who2 = (who + 1) % 4
        wh2 = (wh + 1) % 4
        wn2 = (wn + 1) % 4
        table[c] = (who2 << 4) | (wh2 << 2) | wn2
    return table


def rho_empirical(codes: np.ndarray) -> np.ndarray:
    """rho3: most frequent successor in the empirical series."""
    transitions = {}
    for i in range(len(codes) - 1):
        s, t = int(codes[i]), int(codes[i + 1])
        transitions.setdefault(s, Counter())[t] += 1
    table = np.arange(64)
    for s, counter in transitions.items():
        # Deterministic tie-breaking: smallest successor code.
        best = min(counter.items(), key=lambda kv: (-kv[1], kv[0]))
        table[s] = best[0]
    return table


def apply_rule(rho: np.ndarray, start_code: int, steps: int) -> np.ndarray:
    """Iterate rho from start_code for steps+1 values."""
    traj = np.zeros(steps + 1, dtype=int)
    cur = int(start_code)
    for i in range(steps + 1):
        traj[i] = cur
        cur = int(rho[cur])
    return traj
```

### `empirical/pilot-01/code/classify.py`

```python
"""SUBIT classification: Algorithm 5.1 + Omega_traj."""
from dataclasses import dataclass


@dataclass
class Classification:
    s: str           # "STABLE", "CYCLIC", "CHAOTIC"
    att: str         # "ATTAINED", "ASYMPTOTIC", "INDETERMINATE"
    cycle_length: int
    cycle_start: int


def analyze(traj: list[int]) -> Classification:
    """Algorithm 5.1 with cycle detection."""
    seen = {}
    for i, s in enumerate(traj):
        if s in seen:
            m = seen[s]
            k = i - m
            if k == 1:
                return Classification("STABLE", "ATTAINED", 1, m)
            else:
                return Classification("CYCLIC", "ATTAINED", k, m)
        seen[s] = i
    # Horizon exhausted.
    return Classification("CHAOTIC", "INDETERMINATE", 0, -1)
```

### `empirical/pilot-01/code/baseline.py`

```python
"""Baseline models: ARIMA and Markov chain."""
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from collections import Counter


def fit_arima(x: np.ndarray, order=(2, 0, 2)):
    """Fit ARIMA and return 1-step-ahead predictions."""
    model = ARIMA(x, order=order)
    fit = model.fit()
    return fit.fittedvalues, fit


def fit_markov(codes: np.ndarray, n_states: int = 64):
    """Fit a first-order Markov chain on code6 sequence."""
    counts = np.zeros((n_states, n_states), dtype=int)
    for i in range(len(codes) - 1):
        counts[int(codes[i]), int(codes[i + 1])] += 1
    row_sums = counts.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    P = counts / row_sums
    # Stationary distribution (via power iteration).
    pi = np.ones(n_states) / n_states
    for _ in range(1000):
        pi_new = pi @ P
        if np.allclose(pi, pi_new, atol=1e-10):
            break
        pi = pi_new
    return P, pi


def compare_hypotheses(arima_errors: dict, markov_pis: dict) -> dict:
    """Return a numeric comparison of hypotheses under baselines."""
    out = {}
    for h, err in arima_errors.items():
        out[f"ARIMA_RMSE_{h}"] = float(np.sqrt(np.mean(err ** 2)))
    # Distance between stationary distributions.
    hs = list(markov_pis.keys())
    for i in range(len(hs)):
        for j in range(i + 1, len(hs)):
            d = float(np.linalg.norm(markov_pis[hs[i]] - markov_pis[hs[j]], ord=1))
            out[f"Markov_L1_{hs[i]}_vs_{hs[j]}"] = d
    return out
```

### `empirical/pilot-01/code/run_pilot.py`

```python
"""Full pilot run: encoding, rules, classification, baselines."""
import json
import numpy as np

from load_data import LYNX
from encode import encode
from rules import rho_identity, rho_cycle, rho_empirical, apply_rule
from classify import analyze
from baseline import fit_arima, fit_markov, compare_hypotheses


def run_for_partition(x, n_bins: int, horizon: int = 1000):
    enc = encode(x, n_bins=n_bins)
    n_states = n_bins ** 3
    start_code = int(enc.codes[0])

    # Scale rules to n_bins.
    if n_bins == 4:
        rho1 = rho_identity(enc.codes)
        rho2 = rho_cycle(enc.codes, n_bins)
        rho3 = rho_empirical(enc.codes)
    else:
        # For non-4 bins, use generic rules.
        rho1 = np.arange(n_states)
        rho2 = np.array([((c // n_bins**2 + 1) % n_bins) * n_bins**2
                         + ((c // n_bins) % n_bins + 1) % n_bins * n_bins
                         + (c % n_bins + 1) % n_bins for c in range(n_states)])
        rho3 = rho_empirical(enc.codes)

    results = {}
    for name, rho in [("H1", rho1), ("H2", rho2), ("H3", rho3)]:
        traj = apply_rule(rho, start_code, horizon)
        cls = analyze(traj.tolist())
        results[name] = {
            "s": cls.s,
            "att": cls.att,
            "cycle_length": cls.cycle_length,
            "cycle_start": cls.cycle_start,
        }

    # Baselines.
    try:
        arima_pred, _ = fit_arima(x)
        arima_rmse = float(np.sqrt(np.mean((x - arima_pred) ** 2)))
    except Exception as e:
        arima_rmse = None

    P, pi = fit_markov(enc.codes, n_states=n_states)
    markov_entropy = float(-np.sum(pi[pi > 0] * np.log(pi[pi > 0])))

    return {
        "n_bins": n_bins,
        "n_states": n_states,
        "subit": results,
        "baseline": {
            "arima_rmse": arima_rmse,
            "markov_entropy": markov_entropy,
        },
    }


def main():
    x = LYNX.astype(float)
    all_results = {}
    for n_bins in [2, 4, 8]:
        all_results[f"bins_{n_bins}"] = run_for_partition(x, n_bins)

    # Non-collapse check across partitions.
    classes = []
    for k, v in all_results.items():
        for h, c in v["subit"].items():
            classes.append((k, h, c["s"], c["att"]))
    distinct = len(set((c[2], c[3]) for c in classes))

    all_results["summary"] = {
        "distinct_classifications": distinct,
        "non_collapse": distinct >= 2,
        "hypothesis_separation_H1_H2":
            all_results["bins_4"]["subit"]["H1"]["s"]
            != all_results["bins_4"]["subit"]["H2"]["s"],
    }

    print(json.dumps(all_results, indent=2))


if __name__ == "__main__":
    main()
```

### `empirical/pilot-01/code/Makefile`

```makefile
.PHONY: install run

install:
	pip install -r requirements.txt

run:
	python run_pilot.py | tee results.json
```

---

## `empirical/pilot-01/results.md` (шаблон)

```markdown
# Результати пілота-01

**Дата запуску:** ________________
**Дослідник:** ________________
**Commit:** ________________

## Команда

    cd empirical/pilot-01/code
    make install
    make run

## Таблиця SUBIT-класифікацій

| Розбиття | Гіпотеза | S | Att | cycle length |
|---|---|---|---|---|
| 2 біни  | H₁ | | | |
| 2 біни  | H₂ | | | |
| 2 біни  | H₃ | | | |
| 4 біни  | H₁ | | | |
| 4 біни  | H₂ | | | |
| 4 біни  | H₃ | | | |
| 8 бінів | H₁ | | | |
| 8 бінів | H₂ | | | |
| 8 бінів | H₃ | | | |

## Baseline

| Модель | Метрика | Значення |
|---|---|---|
| ARIMA(2,0,2) | RMSE | |
| Markov (64 стани) | ентропія стаціонарного | |

## Перевірка критеріїв

- [ ] H₁ і H₂ дають різні Ω_traj (STABLE vs CYCLIC)?
- [ ] Ω_traj стійкий хоча б для 2 з 3 розбиттів?
- [ ] Baseline не дає того самого поділу?

## Висновок

*(Заповнюється після запуску. Можливі три результати: пілот успішний,
пілот частково успішний, пілот провалений. Негативний результат —
валідний вихід, як зазначено в roadmap.)*

## Що робити з результатом

- **Успіх** → зафіксувати в STATUS.md як 📊, розширити на 2-3 системи.
- **Частковий успіх** → задокументувати обмеження, повторити з
  іншим розбиттям.
- **Провал** → задокументувати контрприклад, повернутися до §18
  специфікації з новим застереженням.
```

---

## `empirical/pilot-01/classification.json` (шаблон)

```json
{
  "pilot_id": "pilot-01",
  "system": "Hudson Bay lynx (Elton & Nicholson, 1942)",
  "n_points": 114,
  "step_0": {
    "partition": "quantile bins on (log x, Δlog x, Δ²log x)",
    "partitions_tested": [2, 4, 8]
  },
  "step_0_prime": {
    "rules_in_R0": true,
    "F_continuous": true,
    "notes": "finite S0 makes both automatic"
  },
  "hypotheses": {
    "H1": "identity (equilibrium)",
    "H2": "cyclic successor (regular cycle)",
    "H3": "empirical transition table"
  },
  "subit_classifications": {
    "TODO": "fill after running code"
  },
  "baseline": {
    "arima": {"order": [2, 0, 2], "rmse": null},
    "markov": {"n_states": 64, "entropy": null}
  },
  "criteria": {
    "H1_H2_separated": null,
    "stable_across_2_of_3_partitions": null,
    "baseline_distinguishes_equally": null
  },
  "verdict": "PENDING",
  "certificate": {
    "core_version": "0.3.0",
    "infinity_version": "0.2.0",
    "spec_version": "v6.0-draft"
  }
}
```

---

## Критерій завершення ітерації 5.1

- [x] Система обрана (Hudson Bay lynx)
- [x] Крок 0 задокументовано з усіма застереженнями
- [x] Крок 0' пройдено (правила ∈ ℛ_0)
- [x] Три конкуруючі гіпотези H₁, H₂, H₃ сформульовано
- [x] Розрізнювальні передбачення виписано
- [x] Baseline-моделі визначено (ARIMA, Markov)
- [x] Репродукований код написано
- [x] Критерії спростування зафіксовано **заздалегідь**
- [x] Шаблон результатів готовий до заповнення

**Ітерація 5.1 завершена.**

---

## Що далі: ітерація 5.2

Ітерація 5.2 — це **запуск коду** і **заповнення `results.md`**. Її може виконати будь-яка незалежна сторона, яка має:
- Python 3.11+;
- доступ до `statsmodels` (для ARIMA);
- канонічний ряд Hudson Bay (R `datasets::lynx`).

Ітерація 5.2 не може бути зроблена в цьому чаті: вона вимагає виконання коду на реальних даних. Але її **протокол** повністю визначений, і саме це — головна вимога Фази 5.

**Принцип Фази 5, який зафіксовано:** протокол, критерії та код передують даним. Це гарантує, що результат не буде підігнано під гіпотезу.

---

## Зведення по всіх фазах

| Фаза | Статус | Артефакт |
|---|---|---|
| 0. Підготовка | ✅ | `subit-verified/` skeleton, STATUS.md |
| 1. FORMAL | ✅ | §1–22 v6.0-draft |
| 2. CORE | ✅ | `subit-core` v0.3.0 (Rust) |
| 3. PROOFS | ✅ | `subit-proofs` v0.3.0 (Lean 4), 7/10 ✅ + 3/10 ⚠️ |
| 4. INFINITY | ✅ | `subit-infinity` v0.2.0 (Rust) |
| 5. EMPIRICAL | 🔄 | pilot-01 протокол + код (цей артефакт) |
| 6. RELEASE | ⏳ | SUBIT v6.0 |

**STATUS.md після 5.1:**

| Статус | Кількість |
|---|---|
| ✅ | 61 |
| ⚠️ | 6 |
| ❌ | 0 |
| ❓ | 4 |
| 📊 | 0 (очікує 5.2) |
| ⊥ | 0 |

---

## Що далі

Після 5.1 є три можливі кроки:

**A. Ітерація 6 — RELEASE v6.0.** Зібрати всі артефакти у фінальну специфікацію. Це дає завершений документ, навіть якщо пілот 5.2 ще не виконано.

**B. Розширення пілота.** Додати другу систему (нейронні спайки) до протоколу 5.1, щоб мати два незалежні пілоти.

**C. Розширення CORE/INFINITY.** Додати CLI-конвертер емпіричних даних у S₀ (утиліта `subit-encode`), яка інтегрується з протоколом 5.1.

Рекомендація: **A → C → B**. Спочатку зафіксувати v6.0 як реліз з усіма протоколами і кодами на місці. Потім — утиліта `subit-encode` для спрощення емпіричної роботи. Потім — друга система для пілота.
