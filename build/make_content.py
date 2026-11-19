"""Combine everything into ../app/content.json.
Run order:  python3 export.py && python3 mcq.py && python3 explain.py && python3 boards.py && python3 make_content.py
Each step re-checks its answers with real Python and stops on any mismatch."""
import json, os
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app")
J = lambda n: json.load(open(os.path.join(A, n)))
nbs, mcq, why, boards = J("notebooks.json"), J("mcq.json"), J("explain.json"), J("boards.json")
old = J("content.json") if os.path.exists(os.path.join(A, "content.json")) else {"mcq": [], "cards": []}
lab = {x["id"]: x.get("lab", 0) for x in old["mcq"] + old["cards"]}  # lab-safe flags come from tests/br_fidelity.js

SEC = {1: ['mod.import']*3 + ['mod.math','mod.random','mod.platform','mod.own','mod.own','mod.pkg','mod.pip'],
       2: ['str.code','str.seq','str.seq','str.methods','str.cmp','str.cmp','str.cmp'],
       3: ['exc.try','exc.try','exc.tree','exc.raise','exc.raise','exc.else','exc.obj','exc.obj'],
       4: ['oop.basics']*3 + ['oop.private','oop.private','oop.classvar','oop.intro','oop.basics','oop.intro','oop.poly','oop.intro','oop.inherit','oop.mro','oop.poly','oop.inherit'],
       5: ['misc.gen','misc.gen','misc.comp','misc.lambda','misc.lambda','misc.closure','misc.files','misc.files','misc.files','misc.bytes','misc.osdt','misc.osdt','misc.osdt'],
       6: ['bonus.extras']*11}
CH = {1:'mod',2:'str',3:'exc',4:'oop',5:'misc',6:'bonus'}
TOPICS = {
 'mod.import':'Import forms & aliases','mod.math':'math module','mod.random':'random module','mod.platform':'platform module','mod.own':'Your own modules, __name__, sys.path','mod.pkg':'Packages & __init__.py','mod.pip':'pip & PyPI',
 'str.code':'ASCII, Unicode, UTF-8','str.seq':'Slicing & immutability','str.methods':'String methods','str.cmp':'Comparing & sorting',
 'exc.try':'try / except order','exc.tree':'Exception hierarchy','exc.raise':'raise & assert','exc.else':'else & finally','exc.obj':'Exception objects & custom',
 'oop.basics':'Classes, self, __init__','oop.private':'Private names & mangling','oop.classvar':'Class vs instance variables','oop.intro':'hasattr, __dict__, __name__, __bases__','oop.inherit':'Inheritance & super()','oop.mro':'Multiple inheritance (MRO)','oop.poly':'Polymorphism & __str__',
 'misc.gen':'Generators & yield','misc.comp':'List comprehensions','misc.lambda':'lambda, map, filter','misc.closure':'Closures','misc.files':'Files & streams','misc.bytes':'bytearray','misc.osdt':'os, datetime, calendar',
 'bonus.extras':'31-04 extras'}
chapters, cards = [], []
for c in nbs:
    n, lessons = c['num'], []
    for i, s in enumerate(c['sections']):
        if s['title'].startswith('B. Mock'):
            continue
        t = SEC[n][i]
        lessons.append({'title': s['title'].replace('&amp;', '&'), 't': t, 'html': s['html']})
        cards += [dict(a, t=t, src=f'nb{n}', ls=i) for a in s['asks']]
    for j, a in enumerate(c['selftest']):
        t = (('mod' if j < 6 else 'exc' if j < 11 else 'str' if j < 19 else 'oop' if j < 31 else 'misc') if n == 6 else CH[n])
        cards.append(dict(a, t=t, src='mock6' if n == 6 else f'test{n}', why=''))
    chapters.append({'id': CH[n], 'num': n, 'title': c['title'].replace('&amp;', '&'), 'lessons': lessons})
for i, c in enumerate(cards):
    c['id'] = f'c{i}'; c['lab'] = lab.get(c['id'], 0)
for i, m in enumerate(mcq):
    m['id'] = f'q{i}'; m['why'] = why.get(m['id'], m.get('why', '')); m['lab'] = lab.get(m['id'], 0)
json.dump({'chapters': chapters, 'cards': cards, 'mcq': mcq, 'topics': TOPICS, 'boards': boards},
          open(os.path.join(A, 'content.json'), 'w'), separators=(',', ':'))
print('content.json:', len(chapters), 'chapters,', len(cards), 'cards,', len(mcq), 'questions,', len(boards), 'boards')
