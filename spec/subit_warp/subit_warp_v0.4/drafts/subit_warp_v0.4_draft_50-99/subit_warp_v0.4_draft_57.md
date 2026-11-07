# W53 — Boundary Reconstruction, Quotient Geometry and Completion Families

**Project:** SUBIT-WARP v0.4  
**Audit series:** W48 → W48.1 → W49 → W49.1 → W50 → W51 → W52 → W53  
**Scope:** Boundary injectivity, structural reconstruction, quotient spaces, compactness, completion families  
**Reference:** SUBIT-WARP v0.4 / SUBIT-∞ v6.14.0  
**Reference snapshot:** `2dfcf63dc3e2c8328f71269765ab80804f061352`  
**Audit type:** Independent mathematical analysis  
**Status:** BOUNDARY MAP CHARACTERIZED — STRUCTURAL INFORMATION LOSS PROVED  
**Lean status:** NOT VERIFIED  
**Repository status:** NO CHANGES MADE

---

# 0. EXECUTIVE DETERMINATION

W53 досліджує відображення:

`∂:Tω^pr,+ → K(Σ_b)`,

де:

- `Tω^pr,+` — компактний простір прунованих дерев із внутрішнім коренем;
- `Σ_b=B_b^ℕ` — повний простір нескінченних адрес;
- `K(Σ_b)` — простір непорожніх компактних підмножин `Σ_b`;
- `∂t` — множина нескінченних гілок дерева `t`.

Основні результати:

1. Boundary map не є ін'єктивним на повному просторі `Tω^pr,+`.
2. Існують різні дерева з однаковою межею.
3. Причина неін'єктивності — втрата інформації про листки, відсутні дочірні позиції та мітки листків.
4. Для кожного `t∈Tω^pr,+` множина внутрішніх вузлів точно дорівнює множині скінченних префіксів адрес із `∂t`.
5. Кожна непорожня компактна підмножина `Σ_b` є межею принаймні одного дерева з `Tω^pr,+`.
6. Отже, boundary map є сюр'єктивним.
7. Оскільки boundary map 2-Lipschitz, він неперервний.
8. Образ компактного домену в гаусдорфовому просторі `K(Σ_b)` є компактним і замкненим.
9. Факторпростір `Tω^pr,+` за еквівалентністю однакових меж природно ізоморфний `K(Σ_b)`.
10. Для partial fingerprints можна визначити компактні сімейства можливих меж за умови, що множина прунованих completions непорожня.

**Головний висновок:**

Boundary є повним геометричним представленням префіксної структури нескінченних шляхів, але не повним структурним представленням дерева.

Тому:

`Tree ≠ Boundary(Tree)`,

але:

`PrunedTree / BoundaryEquivalence ≅ K(Σ_b)`.

Це розрізнення має стати нормативним принципом SUBIT-WARP.

---

# PART I. FORMAL SETUP

## 1. Канонічні простори

Нехай:

`B_b={1,…,b}`, `b≥2`.

Скінченні адреси:

`Pos_b=B_b^{<ω}`.

Нескінченні адреси:

`Σ_b=B_b^ℕ`.

Корінь:

`ε∈Pos_b`.

Для адреси `u` позначимо:

`|u|` — її довжину.

Для `ξ∈Σ_b`:

`ξ|n` — префікс довжини `n`.

Простір станів:

`S_A={ABSENT,INTERNAL} ⊔ {LEAF(a):a∈A}`.

Дерево:

`t:Pos_b→S_A`.

У W53 використовуються умови:

**TC-01 — Root admissibility**

`t(ε)≠ABSENT`.

**TC-02 — Absent closure**

`t(u)=ABSENT ⇒ t(u·i)=ABSENT`.

**TC-03 — Leaf closure**

`t(u)=LEAF(a) ⇒ t(u·i)=ABSENT`.

**TC-04 — Pruned continuation**

`t(u)=INTERNAL ⇒ Contω(t,u)`.

Для кореневого дерева:

`t(ε)=INTERNAL`.

Визначимо:

`Tω^pr,+={t∈C_Partial : TC-01…TC-04 and t(ε)=INTERNAL}`.

---

# PART II. THE EXACT INFORMATION CONTAINED IN A BOUNDARY

## 2. Префіксне замикання

Для множини нескінченних адрес `F⊆Σ_b` визначимо:

`Pref(F)={u∈Pos_b : ∃ξ∈F, u≼ξ}`.

Тобто `Pref(F)` містить усі скінченні префікси адрес із `F`.

Якщо `F≠∅`, тоді:

`ε∈Pref(F)`.

Множина `Pref(F)` є prefix-closed:

`u∈Pref(F) ∧ v≼u ⇒ v∈Pref(F)`.

## 3. Теорема 3.1 — Internal skeleton theorem

Для кожного:

`t∈Tω^pr,+`

виконується:

`{u∈Pos_b : t(u)=INTERNAL}=Pref(∂t)`.

### Доведення

Покажемо два включення.

**Перше включення:**

`{u:t(u)=INTERNAL}⊆Pref(∂t)`.

Нехай:

`t(u)=INTERNAL`.

За умовою прунованості:

`Contω(t,u)`.

За скінченного branching та лемою Кеніга існує нескінченне продовження `ξ`, яке починається з `u` і складається лише з INTERNAL-вузлів.

Отже:

`ξ∈∂t`.

Оскільки `u≼ξ`:

`u∈Pref(∂t)`.

**Друге включення:**

`Pref(∂t)⊆{u:t(u)=INTERNAL}`.

Нехай:

`u∈Pref(∂t)`.

Тоді існує:

`ξ∈∂t`

така, що:

`u≼ξ`.

За означенням boundary:

`t(ξ|k)=INTERNAL`

для кожного `k`.

Зокрема:

`t(u)=INTERNAL`.

Отже, обидві множини рівні.

Доведено.

### Наслідок 3.2

Boundary повністю визначає INTERNAL-скелет прунованого дерева.

Це сильніший результат, ніж проста неперервність boundary map.

Він означає, що в межах класу `Tω^pr,+` жоден внутрішній вузол не є прихованим від boundary.

Кожен внутрішній вузол належить хоча б одній нескінченній гілці.

---

# PART III. NON-INJECTIVITY

## 4. Контрприклад: LEAF проти ABSENT

Нехай:

`b=2`.

Розглянемо два дерева `t₁,t₂`.

Для обох:

`t(ε)=INTERNAL`.

Нехай позиція `1` є INTERNAL і продовжується нескінченно лише через адреси:

`1, 11, 111, 1111, …`.

Тобто:

`t₁(1^n)=t₂(1^n)=INTERNAL`

для всіх `n≥1`.

На позиції `2` визначимо:

`t₁(2)=LEAF(a)`,

`t₂(2)=ABSENT`.

Усі інші дочірні позиції визначимо відповідно до умов закриття.

Тоді:

`t₁≠t₂`.

Проте:

`∂t₁=∂t₂={(1,1,1,… )}`.

Отже:

`∂t₁=∂t₂ ⇏ t₁=t₂`.

**Boundary map неін'єктивний.**

## 5. Контрприклад: різні мітки листків

Нехай `a₁≠a₂`.

Побудуємо два дерева, що відрізняються лише міткою одного листка:

`t₁(u)=LEAF(a₁)`,

`t₂(u)=LEAF(a₂)`.

Всі внутрішні вузли та всі нескінченні шляхи збігаються.

Тоді:

`∂t₁=∂t₂`.

Отже, boundary не зберігає leaf labels.

## 6. Загальний висновок про неін'єктивність

На повному просторі кодованих прунованих дерев boundary map не може бути ін'єктивним, якщо:

1. розрізняються ABSENT і LEAF;
2. листки можуть мати мітки;
3. boundary містить лише нескінченні адреси.

Це не технічний недолік конкретної метрики.

Це фундаментальна втрата інформації при переході від дерева до його нескінченних гілок.

---

# PART IV. EXACT CHARACTERIZATION OF THE KERNEL

## 7. Boundary equivalence

Визначимо відношення:

`t∼∂s ⇔ ∂t=∂s`.

Це відношення еквівалентності.

### Теорема 7.1 — Kernel characterization

Для:

`t,s∈Tω^pr,+`

маємо:

`t∼∂s`

тоді й лише тоді, коли:

`∀u∈Pos_b, [t(u)=INTERNAL ⇔ s(u)=INTERNAL]`.

### Доведення

**Напрямок 1.**

Нехай:

`∂t=∂s`.

За теоремою 3.1:

`Internal(t)=Pref(∂t)`,

`Internal(s)=Pref(∂s)`.

Тому:

`Internal(t)=Internal(s)`.

**Напрямок 2.**

Нехай:

`Internal(t)=Internal(s)`.

Тоді нескінченна адреса належить `∂t` тоді й лише тоді, коли кожен її скінченний префікс є INTERNAL-вузлом.

Оскільки INTERNAL-скелети однакові, критерій належності до обох меж однаковий.

Отже:

`∂t=∂s`.

Доведено.

## 8. Наслідок: що саме втрачається

Boundary equivalence ігнорує:

- відмінність ABSENT / LEAF;
- мітки `LEAF(a)`;
- будь-яку додаткову інформацію, закодовану лише в листках.

Водночас вона зберігає:

- root;
- усі INTERNAL-адреси;
- префіксну структуру нескінченних шляхів;
- множину всіх нескінченних гілок.

Це точна характеристика ядра boundary map.

---

# PART V. SURJECTIVITY

## 9. Конструкція дерева з довільної компактної межі

Нехай:

`F∈K(Σ_b)`.

Тобто `F` — непорожня компактна підмножина `Σ_b`.

Оскільки `Σ_b` є компактним метричним простором, `F` замкнена.

Побудуємо дерево `t_F`:

`t_F(u)=INTERNAL` тоді й лише тоді, коли `u∈Pref(F)`.

Для решти адрес:

`t_F(u)=ABSENT`.

Тоді:

1. корінь INTERNAL, бо `F≠∅`;
2. INTERNAL-адреси prefix-closed;
3. кожен INTERNAL-вузол має нескінченне продовження, оскільки `u∈Pref(F)`;
4. кожна нескінченна адреса з boundary належить F.

### Теорема 9.1 — Boundary surjectivity

Для кожного:

`F∈K(Σ_b)`

існує:

`t_F∈Tω^pr,+`

таке, що:

`∂t_F=F`.

### Доведення

За побудовою:

`Internal(t_F)=Pref(F)`.

Нехай:

`ξ∈∂t_F`.

Тоді кожен префікс `ξ|n` належить `Pref(F)`.

Отже, для кожного `n` існує:

`η_n∈F`

така, що:

`η_n|n=ξ|n`.

Тому:

`d_Σ(η_n,ξ)≤2^(−n)`.

Отже:

`η_n→ξ`.

Оскільки `F` замкнена:

`ξ∈F`.

Маємо:

`∂t_F⊆F`.

Зворотне включення очевидне: якщо `ξ∈F`, то всі її префікси належать `Pref(F)`, тому:

`ξ∈∂t_F`.

Отже:

`∂t_F=F`.

Доведено.

### Висновок

`∂(Tω^pr,+)=K(Σ_b)`.

Boundary map є сюр'єктивним.

---

# PART VI. CANONICAL REPRESENTATIVE

## 10. Канонічний reduced tree

Конструкція `t_F` визначає канонічного представника кожної boundary equivalence class.

Визначимо:

`R:K(Σ_b)→Tω^pr,+`

так:

`R(F)=t_F`.

Тобто:

- INTERNAL тоді й лише тоді, коли адреса є префіксом F;
- усі інші позиції ABSENT;
- листки не використовуються.

Тоді:

`∂(R(F))=F`.

Отже:

`∂∘R=id_K`.

Це означає, що `R` є правим оберненням boundary map.

## 11. Результат про канонічне представлення

Кожна непорожня компактна boundary має канонічний reduced tree.

Але цей reduced tree не обов'язково є початковим деревом, з якого boundary була отримана.

Він є нормалізованим представником класу еквівалентності.

### Важливе обмеження

Канонічна нормалізація втрачає:

- листки;
- мітки листків;
- відмінність між завершеним дочірнім вузлом і відсутньою позицією.

Тому `R` не є реконструкцією початкового дерева.

Це реконструкція його boundary skeleton.

---

# PART VII. QUOTIENT SPACE

## 12. Факторпростір

Визначимо:

`Q=Tω^pr,+ / ∼∂`.

Елемент Q — клас усіх прунованих дерев з однаковою межею.

Визначимо відображення:

`Φ:Q→K(Σ_b)`

формулою:

`Φ([t])=∂t`.

За характеристикою ядра Φ коректно визначене.

### Теорема 12.1 — Quotient bijection

`Φ:Q→K(Σ_b)` є бієкцією.

**Ін'єктивність.**

Якщо:

`Φ([t])=Φ([s])`,

то:

`∂t=∂s`.

Отже:

`t∼∂s`.

Тому:

`[t]=[s]`.

**Сюр'єктивність.**

Випливає з теореми 9.1.

Отже, Φ є бієкцією.

## 13. Quotient metric

На Q визначимо:

`d_Q([t],[s])=d_H,Σ(∂t,∂s)`.

Це коректно визначена метрика.

Вона не залежить від вибору представників.

Позитивна визначеність випливає з того, що нульова відстань Гаусдорфа між компактними множинами означає їхню рівність.

Отже:

`d_Q([t],[s])=0 ⇔ [t]=[s]`.

### Теорема 13.1 — Quotient isometry

Відображення:

`Φ:(Q,d_Q)→(K(Σ_b),d_H,Σ)`

є ізометрією.

Це випливає безпосередньо з визначення `d_Q`.

**Результат:**

`Tω^pr,+ / ∼∂ ≅ K(Σ_b)`.

Це центральна геометрична теорема W53.

---

# PART VIII. COMPACTNESS OF THE IMAGE

## 14. Неперервність boundary map

За W52:

`d_H,Σ(∂f,∂g)≤2d_F(f,g)`.

Отже, boundary map 2-Lipschitz.

Тому він неперервний.

## 15. Компактність образу

За W52:

`Tω^pr,+`

є компактним.

Неперервний образ компактного простору компактний.

Тому:

`∂(Tω^pr,+)`

компактний у `K(Σ_b)`.

Але за теоремою 9.1:

`∂(Tω^pr,+)=K(Σ_b)`.

Отже:

`K(Σ_b)` компактний.

Це також узгоджується з теоремою Блашке: простір непорожніх компактних підмножин компактного метричного простору є компактним щодо метрики Гаусдорфа.

## 16. Замкненість образу

Простір `K(Σ_b)` є метричним, а отже гаусдорфовим.

Компактна підмножина гаусдорфового простору замкнена.

Тому:

`∂(Tω^pr,+)`

є замкненим.

Оскільки він збігається з усім `K(Σ_b)`, твердження є безпосереднім.

**Статус:** PROVED.

---

# PART IX. METRIC CONSEQUENCES

## 17. Метрика між boundary objects

Для:

`F,G∈K(Σ_b)`

використовуємо:

`d_H,Σ(F,G)`.

За ізометрією факторпростору ця метрика є точною метрикою геометричного quotient SUBIT-WARP.

Вона не вимірює відмінності між деревами, які мають однакову boundary.

## 18. Псевдометрика на початковому просторі

На `Tω^pr,+` визначимо:

`d_∂(t,s)=d_H,Σ(∂t,∂s)`.

Тоді:

`d_∂(t,s)≤2d_F(t,s)`.

`d_∂` є псевдометрикою, а не метрикою, оскільки:

`t≠s`

може поєднуватися з:

`d_∂(t,s)=0`.

Після факторизації за `∼∂` вона стає метрикою.

## 19. Чи існує зворотна Lipschitz-оцінка?

Питання:

`d_F(t,s)≤C·d_H,Σ(∂t,∂s)`

для деякої універсальної сталої C.

На повному просторі `Tω^pr,+` відповідь негативна.

Якщо:

`∂t=∂s`

але:

`t≠s`,

то:

`d_H,Σ(∂t,∂s)=0`,

тоді як:

`d_F(t,s)>0`.

Отже, жодна скінченна C не може задовольнити таку оцінку на повному просторі.

Навіть після факторизації питання про обернену Lipschitz-оцінку потребує окремого аналізу конкретних метрик і нормалізацій.

## 20. Наслідок для реконструкції

Boundary map стискає геометрію дерева.

Вона може відображати структурно різні дерева в одну й ту саму boundary.

Тому:

- forward stability — доведена;
- injectivity — спростована;
- inverse stability — неможлива на повному просторі;
- quotient geometry — повністю визначена.

---

# PART X. COMPLETION FAMILIES

## 21. Partial fingerprint

Нехай:

`F=(P,A;𝒯_allowed)`

є partial fingerprint.

Позначимо:

`Comp(F)={T∈𝒯_allowed : P⊆T, A∩T=∅}`.

Для W53 необхідно відокремити всі допустимі completions від прунованих completions.

Визначимо:

`Comp_pr(F)=Comp(F)∩Tω^pr,+`.

Умова:

`Comp_pr(F)≠∅`

є окремою вимогою.

Непорожність `Comp(F)` не гарантує непорожності `Comp_pr(F)`.

Наприклад, fingerprint може мати лише скінченні completions.

## 22. Boundary completion family

Визначимо:

`B(F)={∂T:T∈Comp_pr(F)}`.

Тоді:

`B(F)⊆K(Σ_b)`.

Це множина всіх можливих меж прунованих completions.

Її не слід ототожнювати з boundary одного completion.

## 23. Компактність completion family

Припустимо:

1. `C_Partial` компактний;
2. constraints fingerprint визначають замкнену множину;
3. `Comp_pr(F)` непорожня;
4. `Tω^pr,+` замкнений.

Тоді:

`Comp_pr(F)`

є замкненою підмножиною компактного простору.

Отже, вона компактна.

Оскільки boundary map неперервний:

`B(F)=∂(Comp_pr(F))`

також компактна.

### Теорема 23.1

За зазначених умов:

`B(F)∈K(K(Σ_b))`.

Тут `K(K(Σ_b))` — простір непорожніх компактних підмножин простору `K(Σ_b)`.

**Статус:** PROVED UNDER CLOSED-CONSTRAINT ASSUMPTIONS.

---

# PART XI. METRIC BETWEEN COMPLETION FAMILIES

## 24. Second-order Hausdorff metric

Нехай:

`B(F),B(G)∈K(K(Σ_b))`.

Визначимо:

`d_H^(2)(B(F),B(G))`

як метрику Гаусдорфа на просторі `K(Σ_b)`, де відстанню між двома boundary objects є `d_H,Σ`.

Тобто:

`d_H^(2)(B(F),B(G)) =`

`max {`

`sup_(A∈B(F)) inf_(C∈B(G)) d_H,Σ(A,C),`

`sup_(C∈B(G)) inf_(A∈B(F)) d_H,Σ(A,C)`

`}`.

Це природна метрика між сімействами можливих меж.

## 25. Залежність від метрики fingerprints

Для двох fingerprint-об'єктів F та G необхідно окремо визначити метрику:

`d_FP(F,G)`.

Без такого означення не можна заявляти Lipschitz-стабільність completion-family map:

`F↦B(F)`.

Проте якщо задано відображення:

`R_F:Comp_pr(F)→Comp_pr(G)`

із контрольованою відстанню між відповідними деревами, тоді можна отримати оцінки для boundary families через W52.

### Умовний результат

Якщо для кожного `T∈Comp_pr(F)` існує:

`S∈Comp_pr(G)`

таке, що:

`d_F(T,S)≤δ`,

і симетрична умова виконується для всіх `S∈Comp_pr(G)`, то:

`d_H^(2)(B(F),B(G))≤2δ`.

Це прямий наслідок 2-Lipschitz continuity boundary map.

**Статус:** CONDITIONAL THEOREM.

---

# PART XII. POSSIBLE AND CERTAIN BOUNDARIES

## 26. Possible boundary

Визначимо:

`BoundaryPossible(F)=⋃_(K∈B(F)) K`.

Це множина адрес, що належать межі хоча б одного completion.

## 27. Certain boundary

Визначимо:

`BoundaryCertain(F)=⋂_(K∈B(F)) K`.

Це множина адрес, що належать межі кожного completion.

Маємо:

`BoundaryCertain(F)⊆BoundaryPossible(F)`.

Однак ці множини мають різну топологічну поведінку.

## 28. Компактність possible boundary

Оскільки:

`B(F)∈K(K(Σ_b))`,

розглянемо incidence relation:

`I={(K,ξ)∈B(F)×Σ_b : ξ∈K}`.

Вона замкнена, оскільки належність до компактної множини є замкненою умовою у просторі компактних підмножин із метрикою Гаусдорфа.

Добуток:

`B(F)×Σ_b`

компактний.

Отже, I компактна.

Проєкція I на `Σ_b` компактна.

Але ця проєкція дорівнює:

`BoundaryPossible(F)`.

Тому:

`BoundaryPossible(F)` компактна.

## 29. Certain boundary

`BoundaryCertain(F)` є перетином замкнених множин.

Тому вона замкнена в `Σ_b`.

Оскільки `Σ_b` компактний:

`BoundaryCertain(F)` компактна, якщо вона непорожня.

Але вона може бути порожньою.

### Приклад

Нехай fingerprint має два pruned completions:

`T₁` з межею:

`∂T₁={111…}`,

`T₂` з межею:

`∂T₂={222…}`.

Тоді:

`BoundaryPossible(F)={111…,222…}`,

але:

`BoundaryCertain(F)=∅`.

Отже, непорожність кожної окремої boundary не гарантує непорожності їхнього перетину.

## 30. Інформаційна інтерпретація

- `BoundaryPossible` — максимальна множина потенційних нескінченних шляхів.
- `BoundaryCertain` — мінімальна множина шляхів, гарантованих усіма completions.
- Різниця між ними — область граничної невизначеності.

Ці об'єкти не є заміною node-level статусів PRESENT / ABSENT / UNKNOWN.

Вони описують невизначеність іншого рівня — рівня нескінченних шляхів.

---

# PART XIII. RECONSTRUCTION LEVELS

## 31. Три рівні реконструкції

W53 встановлює необхідність розділяти три типи реконструкції.

### Level 1 — Structural reconstruction

Вхід:

`F_rec=(L,h,a)`.

Вихід:

повне rooted tree з parent relation.

Це задача W49.1 / T-020.

Вона використовує depth та common-ancestor information.

### Level 2 — Boundary skeleton reconstruction

Вхід:

`F∈K(Σ_b)`.

Вихід:

`R(F)`.

Реконструюється лише префіксна структура нескінченних шляхів.

Це задача W53.

### Level 3 — Partial completion reconstruction

Вхід:

`F_partial`.

Вихід:

`Comp(F_partial)` або:

`Comp_pr(F_partial)`.

Це множина допустимих completions, а не одне дерево.

Відповідний boundary-level вихід:

`B(F_partial)`.

Ці три задачі не можна об'єднувати в одну теорему реконструкції.

## 32. Відсутність загальної boundary reconstruction theorem

З boundary неможливо відновити:

- leaf labels;
- leaf/absent distinction;
- початкову історію утворення дерева;
- інші метадані, що не впливають на нескінченні шляхи.

Тому твердження:

`∂t ⇒ t`

є хибним без додаткових обмежень.

Коректне твердження:

`∂t ⇒ InternalSkeleton(t)`.

---

# PART XIV. CANONICAL REDUCTION AND MODEL DESIGN

## 33. Рекомендована нормалізація

Для геометричних операцій SUBIT-WARP доцільно використовувати:

`ReducedTree(t)=R(∂t)`.

Це дерево, яке містить лише INTERNAL-префікси нескінченних гілок.

Воно є канонічним представником boundary equivalence class.

## 34. Застосування нормалізації

Нормалізація може використовуватися для:

- порівняння геометрії boundary;
- стабільного обчислення Hausdorff distance;
- побудови quotient space;
- класифікації прунованих дерев;
- аналізу граничних множин;
- зменшення структурної надлишковості.

Вона не повинна замінювати початкове дерево в задачах, де важливі листки або їхні мітки.

## 35. Два паралельні представлення

Рекомендується підтримувати:

**Structural representation**

`T_struct`

Містить повну інформацію про:

- INTERNAL;
- LEAF;
- ABSENT;
- leaf labels;
- provenance;
- додаткові метадані.

**Boundary representation**

`T_boundary=R(∂T_struct)`.

Містить лише нескінченний префіксний скелет.

Зв'язок:

`T_struct → T_boundary → ∂T_struct`.

Другий і третій об'єкти є геометричними представленнями, але не замінюють структурного джерела.

---

# PART XV. THEOREM REGISTRY UPDATE

## 36. T-007^pr — Boundary stability

**Домен:** `Tω^pr,+`.

**Формула:**

`d_H,Σ(∂f,∂g)≤2d_F(f,g)`.

**Статус:** PROVED IN W52.

## 37. T-022 — Internal skeleton reconstruction

**Формула:**

`Internal(t)=Pref(∂t)`.

**Статус:** PROVED.

## 38. T-023 — Boundary non-injectivity

**Формула:**

`∃t≠s : ∂t=∂s`.

**Статус:** PROVED BY COUNTEREXAMPLE.

## 39. T-024 — Kernel characterization

**Формула:**

`∂t=∂s ⇔ Internal(t)=Internal(s)`.

**Статус:** PROVED.

## 40. T-025 — Boundary surjectivity

**Формула:**

`∂(Tω^pr,+)=K(Σ_b)`.

**Статус:** PROVED.

## 41. T-026 — Quotient isometry

**Формула:**

`Tω^pr,+/∼∂ ≅ K(Σ_b)`.

**Статус:** PROVED.

## 42. T-027 — Compactness of boundary image

**Формула:**

`∂(Tω^pr,+)` compact and closed in `K(Σ_b)`.

**Статус:** PROVED.

## 43. T-028 — Compact completion boundary family

**Формула:**

`Comp_pr(F)` compact ⇒ `B(F)` compact.

**Статус:** PROVED UNDER CLOSED-CONSTRAINT ASSUMPTIONS.

## 44. T-029 — Possible boundary compactness

**Формула:**

`BoundaryPossible(F)` compact.

**Статус:** PROVED UNDER COMPACT COMPLETION-FAMILY ASSUMPTIONS.

## 45. T-030 — Certain boundary closedness

**Формула:**

`BoundaryCertain(F)` closed, possibly empty.

**Статус:** PROVED.

## 46. T-031 — Completion-family metric stability

**Формула:**

`d_H^(2)(B(F),B(G))≤2δ`.

**Статус:** CONDITIONAL ON TWO-SIDED COMPLETION MATCHING.

---

# PART XVI. RELEASE ACCEPTANCE CRITERIA

## 47. Mathematical requirements

1. Зафіксувати `Internal(t)=Pref(∂t)` як окрему теорему.
2. Зафіксувати неін'єктивність boundary map.
3. Зафіксувати точну характеристику kernel.
4. Зафіксувати сюр'єктивність на `K(Σ_b)`.
5. Зафіксувати quotient isometry.
6. Не заявляти реконструкцію повного дерева з boundary.
7. Відокремити structural representation від boundary representation.
8. Визначити `Comp_pr(F)` окремо від `Comp(F)`.
9. Визначити boundary completion family.
10. Відокремити possible та certain boundary.
11. Не заявляти непорожність certain boundary без додаткових умов.
12. Не заявляти completion-family stability без метрики fingerprint та matching condition.

## 48. Formalization requirements

Майбутня Lean-структура повинна розрізняти:

- `TreeCode`;
- `InternalSkeleton`;
- `Boundary`;
- `BoundaryEquiv`;
- `BoundaryQuotient`;
- `CompactBoundary`;
- `CompletionSet`;
- `PrunedCompletionSet`;
- `BoundaryCompletionFamily`.

Окремо потрібно формалізувати:

1. prefix closure;
2. infinite continuation;
3. König's lemma для скінченного branching;
4. boundary compactness;
5. internal skeleton equality;
6. boundary kernel;
7. canonical representative;
8. surjectivity;
9. quotient metric;
10. completion-family compactness.

Жоден із цих пунктів не вважається Lean-verified лише на підставі математичного тексту.

---

# PART XVII. FINAL AUDIT DECISION

## 49. W53 verdict

| Твердження | Результат |
|---|---|
| Boundary map injective | FALSE |
| Boundary map surjective | PROVED |
| Internal skeleton determined by boundary | PROVED |
| Leaf labels determined by boundary | FALSE |
| ABSENT/LEAF distinction determined by boundary | FALSE |
| Kernel characterization | PROVED |
| Canonical reduced representative | PROVED |
| Quotient isometry | PROVED |
| Boundary image compact | PROVED |
| Boundary image closed | PROVED |
| Completion boundary family compact | CONDITIONAL PROOF |
| Possible boundary compact | PROVED UNDER COMPACTNESS |
| Certain boundary closed | PROVED |
| Certain boundary nonempty | NOT GENERAL |
| Completion-family metric stability | CONDITIONAL |
| Lean verification | NOT VERIFIED |
| GitHub modifications | NONE |

## 50. Final conclusion

W53 встановлює, що boundary map SUBIT-WARP має не структуру повної реконструкції, а структуру геометричного quotient.

Вона:

- зберігає всі нескінченні шляхи;
- зберігає весь INTERNAL-скелет;
- втрачає листки та їхні мітки;
- є сюр'єктивною на простір непорожніх компактних меж;
- є 2-Lipschitz на прунованому домені;
- після факторизації стає ізометрією з `K(Σ_b)`.

Це дає точну математичну формулу:

`Tω^pr,+ / ∼∂ ≅ K(Σ_b)`.

Отже, boundary geometry є не просто наближеним образом дерева, а повним геометричним представленням його класу за boundary equivalence.

Проте вона не є повним структурним представленням початкового дерева.

**W53:** MATHEMATICAL CHARACTERIZATION ACCEPTED.

**T-022…T-030:** ACCEPTED AT MATHEMATICAL LEVEL.

**T-031:** CONDITIONAL.

**SUBIT-WARP v0.4:** RELEASE BLOCK REMAINS IN FORCE UNTIL CANONICAL SPECIFICATION SYNCHRONIZATION AND INDEPENDENT IMPLEMENTATION AUDIT.

**Lean:** NOT VERIFIED.

**GitHub:** NO CHANGES MADE.

---

# 51. NEXT STEP — W54

**W54 — Boundary Quotient, Tree Reconstruction and Information Preservation**

Наступний аудит повинен перейти від геометричної характеристики boundary до інформаційної структури SUBIT-WARP.

Завдання:

1. визначити мінімальний додатковий набір даних, необхідний для відновлення повного дерева;
2. перевірити, чи достатньо пари `(∂t, LeafData(t))`;
3. визначити точний формат LeafData;
4. дослідити, чи можна відновити ABSENT/LEAF distinction без надлишкового збереження всіх координат;
5. визначити умови, за яких boundary map стає ін'єктивним на нормалізованому класі;
6. побудувати reconstruction theorem для enriched boundary;
7. відокремити геометричну інформацію від provenance та історії побудови;
8. перевірити, чи зберігає enriched representation компактність;
9. визначити, які поля мають бути частиною математичного об'єкта, а які — лише metadata;
10. узгодити результат із принципом SUBIT-∞: **DO NOT COLLAPSE — CONTEXTUALIZE**.

**Ключове питання W54:**

Який найменший контекст потрібно додати до boundary, щоб геометричний образ перестав бути втратою структурної інформації?