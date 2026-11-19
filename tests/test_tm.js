const { chromium } = require('playwright'); const path = require('path');
const dir = process.argv[2];
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const [name, vp, scheme] of [['phone', { width: 390, height: 844 }, 'light'], ['desk', { width: 1280, height: 860 }, 'dark']]) {
    const ctx = await b.newContext({ viewport: vp, colorScheme: scheme }); const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    p.on('console', m => { if (m.type() === 'error' && !/net::|Failed to load/.test(m.text())) errs.push(name + ' console: ' + m.text()); });
    await p.route('**/*', r => { const u = r.request().url();
      if (u.includes('fonts.googleapis')) return r.fulfill({ path: path.join(dir, 'fonts.css'), contentType: 'text/css' });
      if (u.includes('confetti')) return r.fulfill({ body: 'window.confetti=function(){}', contentType: 'application/javascript' });
      if (u.startsWith('http://localhost')) return r.continue(); return r.abort(); });
    await p.goto('http://localhost:8765/test.html#learn'); await p.waitForTimeout(700);
    await p.screenshot({ path: `${dir}/shots/${name}-learnhome.png` });
    await p.click('[data-tm]'); await p.waitForTimeout(3500);
    await p.screenshot({ path: `${dir}/shots/${name}-b1s1.png` });
    for (let i = 1; i < 7; i++) {
      await p.click('[data-next]'); await p.waitForTimeout(i === 3 ? 600 : 300);
      if (i === 3) await p.screenshot({ path: `${dir}/shots/${name}-b1s4-mid.png` });
      await p.waitForTimeout(3200);
      if (i === 3 || i === 4) await p.screenshot({ path: `${dir}/shots/${name}-b1s${i + 1}.png` });
    }
    await p.click('[data-try] >> nth=0'); await p.waitForTimeout(800);
    while (await p.$('.modal')) { await p.click('.modal [data-close]'); await p.waitForTimeout(150); }
    await p.screenshot({ path: `${dir}/shots/${name}-b1try.png` });
    await p.click('[data-prev]'); await p.waitForTimeout(300);
    await p.click('[data-next]'); await p.waitForTimeout(500);
    await p.click('[data-done]'); await p.waitForTimeout(800);
    while (await p.$('.modal')) { await p.click('.modal [data-close]'); await p.waitForTimeout(150); }
    await p.screenshot({ path: `${dir}/shots/${name}-chapter.png`, fullPage: true });
    // walk every board to the end to catch rendering errors
    for (const id of ['oop2', 'oop3', 'oop4', 'oop5', 'oop6', 'oop7', 'oop8']) {
      await p.click(`[data-board="${id}"]`); await p.waitForTimeout(300);
      while (await p.$('[data-next]')) { await p.click('[data-next]'); await p.waitForTimeout(120); }
      if (id === 'oop7' || id === 'oop3') { await p.waitForTimeout(3500); await p.screenshot({ path: `${dir}/shots/${name}-${id}-full.png`, fullPage: true }); }
      await p.click('[data-done]'); await p.waitForTimeout(300);
      while (await p.$('.modal')) { await p.click('.modal [data-close]'); await p.waitForTimeout(150); }
    }
    const ow = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1); if (ow) errs.push(name + ' OVERFLOW');
    await p.goto('http://localhost:8765/test.html#today'); await p.waitForTimeout(600);
    await p.screenshot({ path: `${dir}/shots/${name}-today-tm.png` });
    await ctx.close();
  }
  console.log(errs.join('\n') || 'no errors'); await b.close();
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
