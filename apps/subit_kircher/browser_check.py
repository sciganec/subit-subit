"""Браузерні сценарії (Playwright/Chromium). Запуск: python3 tests/test_browser.py   (з каталогу kircher/, після build_atlas.py)."""
import os, re, sys, json, io, contextlib
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
with contextlib.redirect_stdout(io.StringIO()):
    import kircher_model as km
URL = 'file://' + os.path.join(ROOT, 'atlas.html')
fails = []
def check(name, cond, extra=''):
    print(('ok   ' if cond else 'FAIL ') + name + (' — ' + str(extra) if extra and not cond else ''))
    if not cond: fails.append(name)

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 900}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(1500)
    check('lang=uk', pg.evaluate('document.documentElement.lang') == 'uk')
    check('title', 'Людина-Універсум' in pg.title())
    check('старт на сітці', pg.evaluate('location.hash') == '#grid')
    check('ходок не стартує сам', pg.evaluate('GR.playing') is False and pg.evaluate('GR.k') == 0)
    # колесо: Enter і Пробіл
    seg = pg.locator('[data-wr]').first; before = pg.evaluate('state.gridSel')
    targets = pg.evaluate("[...document.querySelectorAll('[data-wr]')].map(g=>g.dataset.wr)")
    check('колесо має 12 сегментів', len(targets) == 12, len(targets))
    moved = False
    for i in range(12):
        s = pg.locator('[data-wr]').nth(i); s.focus(); pg.keyboard.press('Enter'); pg.wait_for_timeout(80)
        if pg.evaluate('state.gridSel') != before: moved = True; break
    check('Enter на сегменті колеса змінює стан', moved)
    s = pg.locator('[data-wr]').nth(5); s.focus(); a = pg.evaluate('state.gridSel'); pg.keyboard.press(' '); pg.wait_for_timeout(80)
    check('Пробіл на сегменті колеса виконується без помилки', not errs)
    # без літер Белнапа на координатах
    detail = pg.inner_text('#gd'); check('літер Белнапа біля координат немає', not re.search(r'WHO \w+ \([TFBN]\)', detail), detail[:200])
    # вкладки: стрілки
    pg.locator('#tabs [aria-selected=true]').focus(); pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(120)
    check('стрілка вправо відкриває наступну вкладку', pg.evaluate('location.hash') == '#timeline', pg.evaluate('location.hash'))
    check('roving tabindex', pg.evaluate("document.querySelectorAll('#tabs [tabindex=\"0\"]').length") == 1)
    pg.keyboard.press('End'); pg.wait_for_timeout(120); check('End → остання вкладка', pg.evaluate('location.hash') == '#about')
    # усі вкладки
    for t in ['grid', 'timeline', 'map', 'model', 'claims', 'network', 'lexicon', 'about']:
        pg.click(f'[data-tab="{t}"]'); pg.wait_for_timeout(150)
        check(f'вкладка {t} відображається', len(pg.inner_text('#main')) > 200)
    # модель: самоперевірка проти Python
    pg.click('[data-tab="model"]'); pg.wait_for_timeout(200); txt = pg.inner_text('#sm').lower()
    check('самоперевірка K^corr і K^ext', txt.count('збігається з протоколом python') == 2, txt[:200])
    py = {}
    for v in ('corr', 'ext'):
        with contextlib.redirect_stdout(io.StringIO()):
            Q, idx, D, Dx, g = km.build(v)
        stats = [km.mp(i, Dx) for i in range(448)]
        py[v] = dict(maxm=max(m for m, _ in stats), maxmp=max(m + q for m, q in stats), n=len(Q))
        js = pg.evaluate(f'(()=>{{const M=MODEL.{v};return {{maxm:M.maxm,maxmp:M.maxmp,n:M.Q.length}}}})()')
        check(f'JS = Python для {v}', js == py[v], (js, py[v]))
    # лексикон
    pg.click('[data-tab="lexicon"]'); pg.fill('#lq', 'арфа'); pg.wait_for_timeout(150)
    check('пошук у лексиконі', 'арф' in pg.inner_text('#lx').lower())
    # реєстр: фільтр допоміжних джерел
    pg.click('[data-tab="claims"]'); pg.click('[data-cw]'); pg.wait_for_timeout(150)
    n_weak = pg.locator('.card').count(); check('фільтр «лише допоміжні» працює', 0 < n_weak < pg.evaluate('D.claims.length'), n_weak)
    check('картка містить статус перевірки', 'Перевірка:' in pg.inner_text('#cl'))
    # сітка: клітини, замок, фільтри
    pg.click('[data-tab="grid"]'); pg.click('[data-gm="tab"]') if pg.locator('[data-gm="tab"]').count() else None
    if pg.locator('.cell').count():
        check('таблиця має 64 клітини', pg.locator('.cell').count() == 64)
        pg.click('.cell[data-cell="10"]'); check('клік по клітині вибирає її', pg.evaluate('state.gridSel') == 10)
        c = pg.locator('.cell[data-cell="20"]').bounding_box(); pg.mouse.move(c['x'] + 8, c['y'] + 8); pg.mouse.down(); pg.wait_for_timeout(650); pg.mouse.up()
        check('довге натискання ставить замок', pg.evaluate('GR.locks.has(20)'))
    # телефон: без горизонтального скролу
    pg.set_viewport_size({'width': 390, 'height': 844})
    for t in ['grid', 'timeline', 'map', 'model', 'claims', 'network', 'lexicon', 'about']:
        pg.click(f'[data-tab="{t}"]'); pg.wait_for_timeout(120)
        check(f'390px без горизонтального скролу: {t}', pg.evaluate('document.documentElement.scrollWidth') <= 390, pg.evaluate('document.documentElement.scrollWidth'))
    check('помилок скрипта немає', not errs, errs)
    b.close()
print('\nПровалів: %d' % len(fails)); sys.exit(1 if fails else 0)
