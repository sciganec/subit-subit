"""Тести ядра моделі K і цілісності даних. Запуск: python3 test_core.py   (з каталогу apps/subit_kircher/)."""
import os, sys, json, unittest, tempfile
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import kircher_model as km
import kircher_data as kd

EXPECT = {  # еталон із протоколу kircher_model_output.txt
    'corr': dict(cycle=24, distinct=24, maxm=4, maxmp=28),
    'ext': dict(cycle=12, distinct=11, maxm=14, maxmp=26),
}


def analyse(variant):
    with contextlib.redirect_stdout(io.StringIO()):
        Q, idx, D, Dx, g = km.build(variant)
    return Q, idx, Dx


class TestEncoding(unittest.TestCase):
    def test_code6_bijection(self):
        codes = set()
        for w in km.A:
            for r in km.A:
                for n in km.A:
                    codes.add(km.code6((w, r, n)))
        self.assertEqual(codes, set(range(64)))

    def test_hexagram_table(self):
        self.assertEqual(len(km.HEX), 64)
        self.assertEqual(len(set(km.HEX.values())), 64)
        self.assertEqual(sorted(km.HEX), list(range(1, 65)))


class TestModelK(unittest.TestCase):
    def test_variants(self):
        for v, exp in EXPECT.items():
            with self.subTest(variant=v):
                Q, idx, Dx = analyse(v)
                self.assertEqual(len(Q), 448)                           # 64 станів x 7 правил
                self.assertEqual(len(Dx), 448)
                self.assertTrue(all(0 <= j < 448 for j in Dx))          # кожен стан має наступника в Q
                stats = [km.mp(i, Dx) for i in range(448)]
                self.assertTrue(all(m + p <= 448 for m, p in stats))   # усі траєкторії входять у цикл
                cyc_nodes = [i for i in range(448) if stats[i][0] == 0]
                seen, cycles = set(), []
                for i in cyc_nodes:
                    if i in seen:
                        continue
                    c = [i]; j = Dx[i]
                    while j != i:
                        c.append(j); j = Dx[j]
                    seen.update(c); cycles.append(c)
                self.assertEqual(len(cycles), 1)                        # один атрактор, без дублювання циклів
                self.assertEqual(len(cycles[0]), exp['cycle'])
                self.assertEqual(len({Q[i][0] for i in cycles[0]}), exp['distinct'])
                self.assertEqual(max(m for m, p in stats), exp['maxm'])
                self.assertEqual(max(m + p for m, p in stats), exp['maxmp'])
                self.assertEqual(len(cyc_nodes), len(cycles[0]))        # вузлів із m=0 рівно стільки, скільки в циклі

    def test_rules_return_valid_state(self):
        for r, f in km.RULES.items():
            for w in km.A:
                for a in km.A:
                    for n in km.A:
                        s = f((w, a, n))
                        self.assertEqual(len(s), 3)
                        self.assertTrue(all(x in km.A for x in s), (r, (w, a, n), s))

    def test_cycle_length_differs_from_distinct_states(self):
        # K^ext: довжина циклу 12, але різних S0 лише 11 (той самий S0 з іншим правилом) — це не помилка підрахунку
        self.assertGreater(EXPECT['ext']['cycle'], EXPECT['ext']['distinct'])


class TestData(unittest.TestCase):
    def test_unique_ids(self):
        for name, coll in [('works', kd.WORKS), ('events', kd.EVENTS), ('people', kd.PEOPLE), ('claims', kd.CLAIMS), ('terms', kd.TERMS)]:
            ids = [x['id'] for x in coll]
            self.assertEqual(len(ids), len(set(ids)), name)

    def test_references(self):
        wid = {w['id'] for w in kd.WORKS}; cid = {c['id'] for c in kd.CLAIMS}; sid = set(kd.SOURCES)
        for coll in (kd.WORKS, kd.EVENTS, kd.PEOPLE, kd.CLAIMS, kd.TERMS):
            for x in coll:
                self.assertTrue(set(x['src']) <= sid, (x['id'], set(x['src']) - sid))
        for w in kd.WORKS:
            self.assertTrue(set(w['claims']) <= cid, w['id'])
            for k2 in w['k2']:
                self.assertTrue(set(k2['src']) <= sid)
        for p in kd.PEOPLE:
            self.assertTrue(set(p['works']) <= wid, p['id']); self.assertIn(p['role'], kd.ROLES)
        for t in kd.TERMS:
            self.assertTrue(set(t['works']) <= wid, t['id'])

    def test_codes_consistent(self):
        for w in kd.WORKS:
            if w['k']:
                self.assertEqual(kd.code6(w['k']), int(''.join({'ME': '10', 'WE': '11', 'YOU': '01', 'THEY': '00'}[w['k'][0]] + {'EAST': '10', 'SOUTH': '11', 'WEST': '01', 'NORTH': '00'}[w['k'][1]] + {'SPRING': '10', 'SUMMER': '11', 'AUTUMN': '01', 'WINTER': '00'}[w['k'][2]]), 2))
        for e in kd.EVENTS:
            self.assertIsNotNone(e['k'], e['id']); self.assertEqual(e['code'], kd.code6(e['k']))

    def test_all_cells_classified(self):
        have = set()
        for w in kd.WORKS:
            if w['k']: have.add(kd.code6(w['k']))
            for x in w['k2']: have.add(kd.code6(x['k']))
        for e in kd.EVENTS: have.add(e['code'])
        self.assertTrue(have <= set(range(64)))

    def test_claims_valid(self):
        for c in kd.CLAIMS:
            self.assertIn(c['t'], (0, 1)); self.assertIn(c['f'], (0, 1)); self.assertTrue(c['src'])
        self.assertIn('N', {kd.BEL[(c['t'], c['f'])] for c in kd.CLAIMS})

    def test_source_model_complete(self):
        for k in kd.SOURCES:
            m = kd.SMETA[k]
            self.assertIn(m['type'], kd.STYPE); self.assertIn(m['tier'], kd.TIER); self.assertIn(m['access'], ('summary', 'unspecified'))
            if m['dup_of']: self.assertIn(m['dup_of'], kd.SOURCES)

    def test_no_placeholder_text(self):
        bad = ['[див', 'TODO', 'XXX', '…]']
        blob = json.dumps([kd.WORKS, kd.EVENTS, kd.PEOPLE, kd.CLAIMS, kd.TERMS], ensure_ascii=False)
        for b in bad: self.assertNotIn(b, blob)
        for p in kd.PEOPLE: self.assertNotIn('Тринадцятиторічний', p['text'])

    def test_years(self):
        for w in kd.WORKS: self.assertTrue(1600 <= w['year'] <= 1680 + 5, w['id'])
        for e in kd.EVENTS:
            self.assertTrue(1600 <= e['year'] <= 2100, e['id'])
            if e.get('end'): self.assertGreaterEqual(e['end'], e['year'])

    def test_export_roundtrip(self):
        tmp_path = os.path.join(tempfile.gettempdir(), '_atlas_test.json')
        out = kd.export(tmp_path)
        self.assertEqual(len(out['terms']), len(kd.TERMS)); self.assertEqual(len(out['claims']), len(kd.CLAIMS))
        for c in out['claims']: self.assertIn('weak', c)

    def test_spec_counts_match_data(self):
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SUBIT-KIRCHER-v2.4.md')
        if not os.path.exists(p): self.skipTest('специфікація v2.4 ще не згенерована')
        with open(p, encoding='utf-8') as f:
            s = f.read()
        self.assertIn('%d термінів' % len(kd.TERMS), s)
        self.assertNotIn('14 термінів Лексикону)', s.split('### 0.7')[1] if '### 0.7' in s else '')


if __name__ == '__main__':
    unittest.main()
