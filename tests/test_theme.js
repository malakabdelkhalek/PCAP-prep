const { chromium } = require('playwright'); const path = require('path'); const dir = process.argv[2];
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } }); const p = await ctx.newPage();
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  await p.route('**/*', r => { const u = r.request().url();
    if (u.includes('fonts.googleapis')) return r.fulfill({ path: path.join(dir, 'fonts.css'), contentType: 'text/css' });
    if (u.includes('confetti')) return r.fulfill({ body: 'window.confetti=function(){}', contentType: 'application/javascript' });
    if (u.startsWith('http://localhost')) return r.continue(); return r.abort(); });
  await p.goto('http://localhost:8765/test.html#today'); await p.waitForTimeout(700);
  await p.click('#thbtn'); await p.waitForTimeout(200); await p.screenshot({ path: `${dir}/shots/th-menu.png` });
  for (const t of ['light', 'dark', 'night']) {
    if (!(await p.$('.thmenu'))) await p.click('#thbtn');
    await p.click(`[data-th="${t}"]`); await p.waitForTimeout(300);
    errs.push(t + ' -> data-theme=' + await p.evaluate(() => document.documentElement.dataset.theme));
    await p.screenshot({ path: `${dir}/shots/th-${t}.png` });
  }
  await p.goto('http://localhost:8765/test.html#learn'); await p.waitForTimeout(600);
  errs.push('after reload: ' + await p.evaluate(() => document.documentElement.dataset.theme));
  await p.click('[data-tm]'); await p.waitForTimeout(3500); await p.screenshot({ path: `${dir}/shots/th-night-board.png` });
  console.log(errs.join('\n')); await b.close();
})();
