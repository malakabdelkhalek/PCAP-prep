const { chromium } = require('playwright'); const fs = require('fs');
const [dir, ver] = [process.argv[2], process.argv[3]];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  p.on('pageerror', e => console.log('PAGEERR', e.message.slice(0, 200)));
  fs.writeFileSync(dir + '/brtest.html', `<html><body><script type="text/python">
from browser import window
import sys
class W:
    def write(self, t):
        window.pyout_(t)
    def flush(self):
        pass
def run(src):
    sys.stdout = W()
    sys.stderr = W()
    g = {'__name__': '__main__'}
    try:
        exec(src, g)
    except BaseException as e:
        window.pyerr_(type(e).__name__, str(e))
window.pyrun = run
window.pyready = True
</script><script src="vendor/${ver}/package/brython.min.js"></script><script src="vendor/${ver}/package/brython_stdlib.js"></script><script>brython({debug:0, indexedDB:false})</script></body></html>`);
  await p.goto('http://localhost:8765/brtest.html');
  await p.waitForFunction(() => window.pyready, null, { timeout: 30000 });
  const C = JSON.parse(fs.readFileSync(dir + '/content.json'));
  const items = process.argv[4] ? JSON.parse(fs.readFileSync(process.argv[4])) : [...C.mcq.filter(q => q.code).map(q => ({ id: q.id, code: q.code, exp: q.ok })), ...C.cards.filter(c => c.code && c.out != null).map(c => ({ id: c.id, code: c.code, exp: c.out }))];
  const t0 = Date.now();
  const res = await p.evaluate(items => items.map(it => { let buf = ''; window.pyout_ = t => buf += t; window.pyerr_ = (n, m) => buf += '!' + n; try { window.pyrun(it.code); } catch (e) { buf += '!JS:' + e.message; } return { id: it.id, got: buf }; }), items);
  const norm = s => s.split('\n').map(l => l.trimEnd()).join('\n').trim();
  const bad = res.filter((r, i) => norm(r.got) !== norm(items[i].exp));
  console.log(ver, 'total', items.length, 'mismatch', bad.length, 'ms', Date.now() - t0);
  bad.slice(0, 40).forEach(r => { const it = items.find(x => x.id === r.id); console.log('--', r.id, JSON.stringify(it.exp).slice(0, 50), '| br:', JSON.stringify(r.got).slice(0, 50)); });
  fs.writeFileSync(`${dir}/br_bad_${ver}.json`, JSON.stringify(bad.map(x => x.id)));
  await b.close();
})();
