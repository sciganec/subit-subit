"""SUBIT-KIRCHER v2.4: математична модель динаміки K (SUBIT-KIRCHER §4)."""

HEXN = {
    '63': 1, '0': 2, '34': 3, '17': 4, '58': 5, '23': 6, '16': 7, '2': 8,
    '59': 9, '55': 10, '56': 11, '7': 12, '47': 13, '61': 14, '8': 15, '4': 16,
    '38': 17, '25': 18, '48': 19, '3': 20, '37': 21, '41': 22, '1': 23, '32': 24,
    '39': 25, '57': 26, '33': 27, '30': 28, '18': 29, '45': 30, '14': 31, '28': 32,
    '15': 33, '60': 34, '5': 35, '40': 36, '43': 37, '53': 38, '10': 39, '20': 40,
    '49': 41, '35': 42, '62': 43, '31': 44, '6': 45, '24': 46, '22': 47, '26': 48,
    '46': 49, '29': 50, '36': 51, '9': 52, '11': 53, '52': 54, '44': 55, '13': 56,
    '27': 57, '54': 58, '19': 59, '50': 60, '51': 61, '12': 62, '42': 63, '21': 64
}
HEX = {v: int(k) for k, v in HEXN.items()}

A = ['10', '11', '01', '00']
G = {'10': '11', '11': '01', '01': '00', '00': '10'}
PHI = {'00': '11', '10': '10', '11': '11', '01': '01'}

RULES = {
    'A': lambda s: ('00', G[s[1]], s[2]),
    'C': lambda s: (G[s[0]], G[s[1]], s[2]),
    'M': lambda s: ('11', G[s[1]], '11'),
    'T': lambda s: (s[0], s[1], G[s[2]]),
    'P': lambda s: ('01', s[1], '00'),
    'X': lambda s: (PHI[s[0]], PHI[s[1]], PHI[s[2]]),
    'K': lambda s: ('10', s[1], '10')
}
RK = ['A', 'C', 'M', 'T', 'P', 'X', 'K']


def code6(s):
    return int(''.join(s), 2)


def st_from_code(n):
    b = bin(n)[2:].zfill(6)
    return (b[0:2], b[2:4], b[4:6])


def gmeta(variant):
    def g(r, s):
        if r == 'A':
            return 'M'
        if r == 'M':
            return 'C'
        if r == 'C':
            return 'T'
        if r == 'T':
            return 'P' if s[2] == '11' else 'A'
        if r == 'P':
            return 'X' if variant == 'ext' else 'K'
        return 'A'
    return g


def build(variant):
    g = gmeta(variant)
    Q = []
    idx = {}
    for n in range(64):
        for r in RK:
            idx[(n, r)] = len(Q)
            Q.append((n, r))
    D = {}
    Dx = []
    for n, r in Q:
        s = st_from_code(n)
        s_next = RULES[r](s)
        n_next = code6(s_next)
        r_next = g(r, s)
        target_idx = idx[(n_next, r_next)]
        D[(n, r)] = (n_next, r_next)
        Dx.append(target_idx)
    return Q, idx, D, Dx, g


def mp(i, Dx):
    vis = {}
    curr = i
    step = 0
    while curr not in vis:
        vis[curr] = step
        step += 1
        curr = Dx[curr]
    m = vis[curr]
    p = step - m
    return m, p
