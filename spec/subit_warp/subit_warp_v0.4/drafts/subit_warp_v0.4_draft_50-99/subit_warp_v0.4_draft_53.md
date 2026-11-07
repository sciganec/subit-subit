# SUBIT-WARP v0.4
## W49.1 — Fingerprint Reconstruction Repair

**Document class:** Mathematical Repair / Reconstruction Theory  
**Audit predecessor:** W49 — Independent Verification of W48.1  
**Patch target:** T-020′ and T-021′  
**Baseline:** SUBIT-WARP v0.4 C2  
**Integration target:** SUBIT-∞ v6.14.0  
**Status:** RECONSTRUCTION FRAMEWORK SPECIFIED — PROOF CONDITIONS EXPLICIT  
**Release status:** BLOCKED PENDING INDEPENDENT VERIFICATION

---

# 0. Мета документа

W49 виявив, що попередня редакція T-020′ не встановлює достатніх умов для єдиної реконструкції rooted tree з unordered fingerprint.

Також було встановлено, що T-021′ не визначає однозначної семантики UNKNOWN для часткових ordered trees.

W49.1 розділяє ці задачі на два математично різні напрями:

**T-020 — Unordered Reconstruction**

Відновлення rooted tree з інформації про глибину вузлів та глибину їхнього спільного предка.

**T-021 — Ordered Partial Reconstruction**

Відновлення впорядкованого дерева з часткової інформації про наявність, відсутність або невизначеність дочірніх позицій.

Основна вимога:

> Реконструкційна теорема повинна визначати не лише умови сумісності fingerprint із деревом, а й конкретний механізм побудови дерева та умови його єдиності.

---

# PART I — T-020: UNORDERED TREE RECONSTRUCTION

# 1. Problem Definition

Нехай L — множина вузлів.

Нехай:

`h : L → ℕ₀`

є функцією глибини.

Нехай:

`a : L × L → ℕ₀`

є функцією спільної глибини.

Інтуїтивно:

`a(x,y) = depth(LCA(x,y))`

де LCA(x,y) — найнижчий спільний предок вузлів x та y.

Однак у задачі реконструкції LCA та parent relation ще не задані.

Тому запис:

`a(x,y)=h(LCA(x,y))`

не може бути використаний як початкова аксіома реконструкції: він уже припускає існування шуканої структури.

Необхідно визначити умови, за яких L та функції h,a самі визначають rooted tree.

---

# 2. Level Decomposition

Для кожного `n∈ℕ₀` визначимо рівень:

`L_n = {x∈L : h(x)=n}`.

Також:

`L_{≥k} = {x∈L : h(x)≥k}`.

Введемо відношення:

`x ≡_k y ⇔ a(x,y)≥k`

для:

`x,y∈L_{≥k}`.

Інтерпретація:

Два вузли еквівалентні на рівні k тоді й лише тоді, коли вони належать до однієї гілки до глибини k.

Ця система еквівалентностей є основою реконструкції.

---

# 3. Reconstruction Axioms

## UFP-01 — Nonempty domain

`L ≠ ∅`.

## UFP-02 — Nonnegative integer depth

`h : L → ℕ₀`.

## UFP-03 — Root existence and uniqueness

Множина:

`L₀={x∈L:h(x)=0}`

містить рівно один елемент.

Позначимо його:

`r`.

## UFP-04 — Symmetry

Для всіх x,y:

`a(x,y)=a(y,x)`.

## UFP-05 — Self-depth

Для всіх x:

`a(x,x)=h(x)`.

## UFP-06 — Common-depth bound

Для всіх x,y:

`0≤a(x,y)≤min(h(x),h(y))`.

## UFP-07 — Equivalence at every level

Для кожного `k∈ℕ₀` відношення:

`x ≡_k y ⇔ a(x,y)≥k`

є відношенням еквівалентності на `L_{≥k}`.

Отже, воно має бути:

- рефлексивним;
- симетричним;
- транзитивним.

Симетричність уже випливає з UFP-04, але вона зберігається в переліку як явна структурна вимога.

## UFP-08 — Unique level representative

Для кожного:

`x∈L_{≥k}`

його клас еквівалентності:

`[x]_k={y∈L_{≥k}:a(x,y)≥k}`

містить рівно один елемент рівня k.

Формально:

`|[x]_k ∩ L_k|=1`.

Цей елемент позначимо:

`π_k(x)`.

Він інтерпретується як предок x на рівні k.

## UFP-09 — Root compatibility

Для кожного x:

`π₀(x)=r`.

Оскільки L₀ містить рівно один елемент, ця умова є наслідком UFP-03 та UFP-08, але вона залишається явною для зручності формальної перевірки.

## UFP-10 — Nested ancestry

Для будь-яких:

`0≤j≤k≤h(x)`

виконується:

`π_j(π_k(x))=π_j(x)`.

Інтерпретація: предок предка є відповідним предком початкового вузла.

## UFP-11 — Exact common-depth reconstruction

Для будь-яких x,y:

`a(x,y)=max{k : π_k(x)=π_k(y)}`.

Це твердження визначає a як точну глибину найнижчого спільного предка, а не лише як функцію, що задовольняє ультраметричну нерівність.

---

# 4. Reconstruction Theorem T-020B

## 4.1. Statement

**T-020B — Unordered Rooted-Tree Reconstruction from Common-Depth Fingerprint**

Нехай задано:

`F_rec=(L,h,a)`.

Якщо виконуються UFP-01…UFP-11, то існує єдина з точністю до ізоморфізму rooted tree:

`T=(L,p)`

з функцією глибини h та функцією спільної глибини a.

Тут p — реконструйоване батьківське відношення.

## 4.2. Construction of parent relation

Для кожного:

`x∈L_n`, де `n>0`,

визначимо:

`parent(x)=π_(n−1)(x)`.

Отже:

`p(x)=π_(h(x)−1)(x)`.

Для кореня:

`parent(r)` не визначається.

Це однозначно задає parent relation.

## 4.3. Proof of existence

Візьмемо довільний вузол:

`x∈L_n`.

За UFP-08 існує рівно один предок на кожному рівні:

`π₀(x), π₁(x), …, π_n(x)`.

За UFP-05 та UFP-08:

`π_n(x)=x`.

За UFP-09:

`π₀(x)=r`.

За UFP-10:

`π_(n−1)(π_n(x))=π_(n−1)(x)`.

Тому:

`parent(x)=π_(n−1)(x)`

є єдиним вузлом глибини n−1, який належить до ancestry chain x.

Повторне застосування parent зменшує глибину рівно на одиницю.

Отже, кожен вузол за скінченну кількість кроків досягає кореня.

Тому структура:

`T=(L,p)`

є rooted tree.

## 4.4. Proof of common-depth consistency

За UFP-11:

`a(x,y)=max{k:π_k(x)=π_k(y)}`.

Але π_k(x) та π_k(y) є предками відповідних вузлів на рівні k.

Отже, максимальне k, для якого вони збігаються, є глибиною найнижчого спільного предка.

Тому:

`a(x,y)=h(LCA_T(x,y))`.

## 4.5. Proof of uniqueness

Нехай існує інше rooted tree:

`T'=(L,p')`

із тією самою функцією глибини h та тією самою функцією спільної глибини a.

У будь-якому rooted tree предок x на рівні k є єдиним вузлом y, для якого:

- `h(y)=k`;
- `a(x,y)=k`.

За UFP-08 та означенням ≡_k такий вузол єдиний і дорівнює π_k(x).

Отже, в T':

`ancestor_k(x)=π_k(x)`.

Тому для кожного x:

`p'(x)=π_(h(x)−1)(x)=p(x)`.

Отже:

`p'=p`.

Реконструйоване дерево є єдиним.

**T-020B proof status:** PROVED UNDER UFP-01…UFP-11.

---

# 5. Remarks on Minimality and Redundancy

Умови UFP-01…UFP-11 не є мінімальним аксіоматичним набором.

Частина з них є наслідками інших.

Наприклад:

- UFP-09 випливає з UFP-03 та UFP-08;
- UFP-10 може бути виведена з вкладеності класів еквівалентності за додаткових умов;
- UFP-11 може бути частково виведена з визначення π_k та відповідної вкладеності.

Однак на цьому етапі специфікації їх доцільно зберегти як явні acceptance conditions.

Мінімізація аксіом повинна бути окремою задачею.

Не можна видаляти умову лише тому, що вона здається надлишковою: спочатку необхідно формально довести її залежність від інших умов.

---

# 6. T-020A — Fingerprint Consistency

T-020A не є реконструкційною теоремою.

Її задача — перевірити, чи відповідають задані дані:

`F_ver=(L,h,a,p)`

одній і тій самій rooted-tree структурі.

## 6.1. Parent relation requirements

Для кожного x, де:

`h(x)>0`,

має існувати рівно один:

`p(x)∈L`

такий, що:

`h(p(x))=h(x)−1`.

Крім того:

`p^n(x)=r`

для `n=h(x)`.

## 6.2. Common-depth consistency

Для всіх x,y:

`a(x,y)=h(LCA_p(x,y))`.

## 6.3. Verification theorem

**T-020A — Fingerprint Consistency Theorem**

Якщо parent relation p є rooted-tree relation, а a збігається з глибиною найнижчого спільного предка відносно p, то:

`F_ver=(L,h,a,p)`

є структурно узгодженим unordered fingerprint.

Це твердження є перевіркою вже заданої структури.

Воно не доводить реконструкцію p з `(L,h,a)`.

**T-020A proof status:** PROVED BY DIRECT VERIFICATION.

---

# PART II — T-021: ORDERED PARTIAL TREE RECONSTRUCTION

# 7. Ordered Address Space

Нехай:

`B_b={1,…,b}`

— скінченний упорядкований алфавіт дочірніх позицій.

Нехай:

`B_b*`

— множина скінченних адрес.

Коренева адреса:

`ε`.

Для адреси u та дочірньої позиції i:

`u·i`

позначає конкатенацію.

Повне або часткове впорядковане дерево описується множиною адрес та правилами її структурної допустимості.

---

# 8. Complete Ordered Trees

Визначимо повне occupied-address tree як множину:

`T⊆B_b*`

що задовольняє:

**OT-01 — Root**

`ε∈T`.

**OT-02 — Prefix closure**

Якщо:

`u·v∈T`,

то кожен префікс адреси `u·v` також належить T.

**OT-03 — Finite branching**

Для кожного u існує не більше b дочірніх позицій.

**OT-04 — Unique address**

Кожна адреса відповідає рівно одному вузлу.

Важливо: T описує множину зайнятих адрес, але не визначає автоматично, чи відсутня позиція є ABSENT або UNKNOWN у частковому описі.

Це різні рівні інформації.

---

# 9. Partial Ordered Fingerprint

Введемо:

`F_partial=(L,p,h,σ)`.

Тут:

- L — множина відомих вузлів;
- p — адреса кожного відомого вузла;
- h — глибина;
- σ — інформаційний статус дочірньої позиції.

Функція:

`σ : B_b* × B_b → {PRESENT, ABSENT, UNKNOWN}`

визначає статус кожної дочірньої позиції відомого або потенційного вузла.

Усі адреси, що не можуть бути дочірніми позиціями внаслідок відомої структурної відсутності предка, також вважаються структурно недопустимими.

---

# 10. Completion Semantics

## 10.1. Definition

Нехай:

`Comp(F_partial)`

— множина всіх повних ordered trees, сумісних із заданим частковим fingerprint.

Кожне:

`T∈Comp(F_partial)`

має задовольняти:

1. T prefix-closed;
2. усі підтверджені адреси присутні;
3. усі підтверджені відсутні адреси відсутні;
4. невідомі позиції можуть бути присутніми або відсутніми;
5. усі відомі parent-child відношення збережені;
6. жодна структурна умова не порушується.

Вимагаємо:

`Comp(F_partial)≠∅`.

Це означає, що частковий fingerprint є принаймні логічно сумісним із деяким повним деревом.

## 10.2. PRESENT

Для позиції `(u,i)`:

`σ(u,i)=PRESENT`

тоді й лише тоді, коли:

`∀T∈Comp(F_partial), u·i∈T`.

Позиція присутня в усіх допустимих завершеннях.

## 10.3. ABSENT

`σ(u,i)=ABSENT`

тоді й лише тоді, коли:

`∀T∈Comp(F_partial), u·i∉T`.

Позиція відсутня в усіх допустимих завершеннях.

## 10.4. UNKNOWN

`σ(u,i)=UNKNOWN`

тоді й лише тоді, коли існують:

`T₁,T₂∈Comp(F_partial)`

такі, що:

`u·i∈T₁`

та:

`u·i∉T₂`.

Отже, існують принаймні два допустимі завершення, які розрізняються щодо цієї позиції.

UNKNOWN означає не третій онтологічний стан вузла, а недостатність інформації для визначення його структурного статусу.

---

# 11. Consistency Constraints for Completion

Щоб множина completions була коректною, необхідні такі умови.

## PC-01 — Root certainty

Корінь завжди присутній:

`ε∈T` для кожного `T∈Comp(F_partial)`.

## PC-02 — Prefix dependency

Якщо адреса:

`u·i`

присутня в T, то u також присутня в T.

## PC-03 — Absence propagation

Якщо u відсутній, то всі його нащадки відсутні.

## PC-04 — Present-child validity

Якщо:

`σ(u,i)=PRESENT`,

то u має бути присутнім у кожному допустимому completion.

## PC-05 — Absent-child exclusion

Якщо:

`σ(u,i)=ABSENT`,

то `u·i` відсутній у кожному допустимому completion.

## PC-06 — Unknown variability

Якщо:

`σ(u,i)=UNKNOWN`,

то існують допустимі completions із присутньою та відсутньою позицією.

## PC-07 — Address consistency

Якщо два відомі вузли мають адреси p(x) та p(y), то:

`x≠y ⇒ p(x)≠p(y)`.

## PC-08 — Depth consistency

Для кожного відомого вузла x:

`h(x)=|p(x)|`.

## PC-09 — Known-prefix consistency

Кожен префікс адреси відомого вузла має бути присутнім у кожному допустимому completion.

## PC-10 — Completion nonemptiness

`Comp(F_partial)≠∅`.

---

# 12. T-021A — Ordered Trie Reconstruction

**Theorem T-021A — Reconstruction of a Complete Ordered Trie**

Нехай задано повний fingerprint:

`F_ord=(L,p,h)`.

Якщо:

1. p ін'єктивне;
2. образ p prefix-closed;
3. коренева адреса ε належить образу p;
4. `h(x)=|p(x)|`;

то існує єдиний occupied ordered trie:

`T=p(L)`.

Доведення безпосереднє.

Множина адрес однозначно визначена образом p.

Prefix closure забезпечує структурну допустимість.

Ін'єктивність p забезпечує відсутність конфліктів адрес.

Отже, реконструкція є єдиною.

**Proof status:** PROVED.

## 12.1. Обмеження

Ця теорема відновлює occupied trie.

Вона не відновлює інформацію про те, чи є кожна відсутня позиція:

- підтверджено відсутньою;
- невідомою;
- не включеною до області спостереження.

Для цього необхідна completion semantics.

---

# 13. T-021B — Partial Completion Theorem

**Theorem T-021B — Completion Semantics of Partial Ordered Fingerprints**

Нехай задано:

`F_partial=(L,p,h,σ)`.

Якщо виконуються PC-01…PC-10, то:

`Comp(F_partial)`

є непорожньою множиною повних ordered trees, сумісних із частковим fingerprint.

Для кожної дочірньої позиції `(u,i)` виконується рівно одна з трьох умов:

1. позиція присутня в усіх completions;
2. позиція відсутня в усіх completions;
3. позиція присутня в одних completions і відсутня в інших.

Ці випадки визначають відповідно:

- PRESENT;
- ABSENT;
- UNKNOWN.

## 13.1. Proof sketch

Оскільки:

`Comp(F_partial)≠∅`,

існує принаймні одне допустиме завершення.

Для фіксованої позиції `(u,i)` розглянемо дві множини:

`C₁={T∈Comp(F_partial):u·i∈T}`

та:

`C₀={T∈Comp(F_partial):u·i∉T}`.

Можливі три випадки:

**Case A**

`C₁=Comp(F_partial)`.

Тоді позиція PRESENT.

**Case B**

`C₀=Comp(F_partial)`.

Тоді позиція ABSENT.

**Case C**

`C₁≠∅` і `C₀≠∅`.

Тоді позиція UNKNOWN.

Оскільки `Comp(F_partial)` непорожня, ці три випадки вичерпують усі можливості.

Вони попарно несумісні.

Отже, семантика є однозначною.

**Proof status:** PROVED AS CLASSIFICATION OF NONEMPTY COMPLETION SETS.

Важливе обмеження: ця теорема не доводить існування completion для довільного набору локальних статусів. Непорожність `Comp(F_partial)` залишається окремою умовою сумісності.

---

# 14. Ontological and Epistemic Separation

T-021 вводить важливе розрізнення.

## 14.1. Ontological structure

Повне дерево T має конкретну структуру:

`u·i∈T` або `u·i∉T`.

Для одного конкретного повного дерева немає третього структурного стану.

## 14.2. Epistemic status

Частковий fingerprint не обов'язково визначає, який із двох структурних варіантів є правильним.

UNKNOWN означає:

`∃T₁,T₂∈Comp(F_partial)`

із різними відповідями щодо відповідної позиції.

Отже:

UNKNOWN — це характеристика інформаційного стану, а не третій фізичний або структурний стан дерева.

## 14.3. SUBIT principle

Це розрізнення відповідає принципу:

**DO NOT COLLAPSE — CONTEXTUALIZE.**

Не можна зводити:

- відсутність;
- невідомість;
- структурну неможливість;
- неповноту спостереження

до одного значення.

---

# PART III — REVISED THEOREM REGISTRY

# 15. Registry After W49.1

| ID | Твердження | Статус |
|---|---|---|
| T-020A | Fingerprint Consistency | PROVED |
| T-020B | Unordered Reconstruction | PROVED UNDER UFP-01…UFP-11 |
| T-021A | Complete Ordered Trie Reconstruction | PROVED |
| T-021B | Partial Completion Classification | PROVED UNDER NONEMPTY COMPLETION |
| T-002 | Compactness of Non-Expanding Maps | PROOF REQUIRED |
| T-004 | Compactness of Σ_b | PROVED |
| T-007 | Boundary Stability | PROVED ON Tω^pr,+ |
| T-014 | Normalized Matrix Row Sum | PROVED UNDER BASIS CONVENTION |
| T-018 | Trace-Norm Approximation | PREVIOUS STATUS — NOT REOPENED |
| T-019 | Global Lipschitz Continuity | PROVED UNDER COMMON SPECTRAL DECOMPOSITION |

---

# 16. Integration Requirements for SUBIT-∞ v6.14.0

Інтеграція повинна зберігати поділ на consistency та reconstruction.

## 16.1. Unordered layer

Рекомендована структура:

`WARP.Tree.Unordered.Fingerprint`

`WARP.Tree.Unordered.Equivalence`

`WARP.Tree.Unordered.Ancestry`

`WARP.Tree.Unordered.Reconstruction`

`WARP.Tree.Unordered.Uniqueness`

## 16.2. Ordered layer

Рекомендована структура:

`WARP.Tree.Ordered.Address`

`WARP.Tree.Ordered.Trie`

`WARP.Tree.Ordered.Partial`

`WARP.Tree.Ordered.Completion`

`WARP.Tree.Ordered.PresentAbsentUnknown`

## 16.3. Integration boundary

T-020A не повинна підміняти T-020B.

T-021A не повинна підміняти T-021B.

T-021B не повинна трактувати UNKNOWN як третій структурний стан.

Жоден із цих результатів не можна автоматично представляти як Lean-verified.

---

# 17. Verification Checklist

**V49.1-AC-01:** Рівні L_n визначені однозначно.

**V49.1-AC-02:** Відношення ≡_k є еквівалентністю.

**V49.1-AC-03:** Кожен клас еквівалентності містить рівно одного представника рівня k.

**V49.1-AC-04:** Parent relation визначається через π_(n−1).

**V49.1-AC-05:** Parent relation завершується коренем.

**V49.1-AC-06:** Функція a збігається з глибиною LCA.

**V49.1-AC-07:** Доведена єдиність unordered reconstruction.

**V49.1-AC-08:** Ordered trie має prefix closure.

**V49.1-AC-09:** PRESENT та ABSENT визначаються відносно всіх completions.

**V49.1-AC-10:** UNKNOWN означає варіативність між допустимими completions.

**V49.1-AC-11:** Множина completions непорожня.

**V49.1-AC-12:** Відмінність онтологічної структури та епістемічного статусу збережена.

**V49.1-AC-13:** Теореми мають статуси, що відповідають фактичним доказам.

---

# 18. Release Gate

W49.1 пропонує математично визначені реконструкційні структури, але не є остаточним дозволом на реліз.

До наступного етапу необхідно:

1. Незалежно перевірити достатність UFP-01…UFP-11.
2. Перевірити, чи можна скоротити аксіоматичний набір без втрати єдиності.
3. Перевірити всі крайові випадки: корінь, unary nodes, finite leaves, нескінченні гілки.
4. Перевірити, що `Comp(F_partial)` визначено як множину структур, а не як неформальну множину можливостей.
5. Перевірити узгодженість UNKNOWN із prefix closure.
6. Перевірити інтеграцію в SUBIT-∞ v6.14.0.
7. Не підвищувати математичний статус до Lean verification без машинного доказу.

---

# 19. Final Assessment

W49.1 розділяє дві задачі, які раніше були об'єднані:

- реконструкцію дерева з глибинної структури;
- реконструкцію впорядкованого дерева з неповної інформації.

Для unordered case введено систему рівневих еквівалентностей:

`x ≡_k y ⇔ a(x,y)≥k`.

Кожен клас має єдиного представника на рівні k. Ці представники визначають ancestry maps π_k, а вони, своєю чергою, однозначно визначають parent relation.

Для ordered partial case введено множину допустимих завершень:

`Comp(F_partial)`.

Статуси PRESENT, ABSENT та UNKNOWN визначаються не довільною локальною домовленістю, а поведінкою відповідної позиції в усіх допустимих completions.

Це створює строгий поділ між структурою дерева та інформацією про дерево.

## Final status

**W49.1:** RECONSTRUCTION FRAMEWORK SPECIFIED.

**T-020A:** PROVED.

**T-020B:** PROVED UNDER UFP-01…UFP-11.

**T-021A:** PROVED.

**T-021B:** PROVED UNDER NONEMPTY COMPLETION.

**WARP v0.4:** RELEASE BLOCKED PENDING INDEPENDENT VERIFICATION.

**SUBIT-∞ v6.14.0:** INTEGRATION PENDING.

**Lean verification:** NOT ESTABLISHED.

**GitHub modifications:** NONE.

**Next phase:** W50 — Independent Verification of Reconstruction Axioms and Completion Semantics.