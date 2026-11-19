const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const dir = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const errs = [];
  for (const [name, vp] of [['phone', { width: 390, height: 844 }], ['desk', { width: 1280, height: 820 }]]) {
    const ctx = await b.newContext({ viewport: vp, colorScheme: name === 'desk' ? 'dark' : 'light' });
    const p = await ctx.newPage();
    const cm = async () => { await p.waitForTimeout(500); while (await p.$('.modal')) { await p.click('.modal [data-close]'); await p.waitForTimeout(150); } };
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    p.on('console', m => { if (m.type() === 'error' && !/ERR_|net::|Failed to load resource/.test(m.text())) errs.push(name + ' console: ' + m.text()); });
    await p.route('**/*', r => {
      const u = r.request().url();
      if (u.includes('brython.min.js')) return r.fulfill({ path: path.join(dir, 'vendor/br13/package/brython.min.js'), contentType: 'application/javascript' });
      if (u.includes('brython_stdlib.js')) return r.fulfill({ path: path.join(dir, 'vendor/br13/package/brython_stdlib.js'), contentType: 'application/javascript' });
      if (u.includes('fonts.googleapis')) return r.fulfill({ path: path.join(dir, 'fonts.css'), contentType: 'text/css' });
      if (u.includes('confetti')) return r.fulfill({ body: 'window.confetti=function(){}', contentType: 'application/javascript' });
      if (u.startsWith('http://localhost')) return r.continue();
      return r.abort();
    });
    await p.goto('http://localhost:8765/test.html#today'); await p.waitForTimeout(800);
    await p.screenshot({ path: `${dir}/shots/${name}-today.png`, fullPage: false });
    // mission 1: diagnostic 20
    await p.click('[data-mission="0"]'); await p.waitForTimeout(200);
    await p.screenshot({ path: `${dir}/shots/${name}-q1.png` });
    for (let i = 0; i < 20; i++) {
      await p.click('.opt >> nth=' + (i % 4)); await p.waitForTimeout(60);
      if (i === 0) await p.screenshot({ path: `${dir}/shots/${name}-fb.png` });
      await p.click('[data-nextq]'); await p.waitForTimeout(60);
    }
    await p.waitForTimeout(300); await p.screenshot({ path: `${dir}/shots/${name}-result.png` }); await cm();
    await p.click('[data-home]'); await p.waitForTimeout(200);
    // close any modal
    while (await p.$('.modal')) { await p.click('.modal [data-close]'); await p.waitForTimeout(100); }
    // mission 2: read lesson
    await p.click('[data-mission="1"]'); await p.waitForTimeout(200);
    await p.screenshot({ path: `${dir}/shots/${name}-lesson.png`, fullPage: true });
    while (await p.$('[data-next]')) { await p.click('[data-next]'); await p.waitForTimeout(80); } await p.click('[data-done]'); await cm();
    while (await p.$('.modal')) { await p.click('.modal [data-close]'); await p.waitForTimeout(100); }
    await p.goto('http://localhost:8765/test.html#weak'); await p.waitForTimeout(600);
    await p.screenshot({ path: `${dir}/shots/${name}-weak.png`, fullPage: true });
    await p.click('a[data-tab="lab"]'); await p.waitForTimeout(200);
    await p.click('#run'); await p.waitForTimeout(5000);
    const out = await p.textContent('#out'); errs.push(name + ' LAB OUTPUT: ' + JSON.stringify(out));
    await p.screenshot({ path: `${dir}/shots/${name}-lab.png` });
    await p.click('a[data-tab="practice"]'); await p.waitForTimeout(200);
    await p.screenshot({ path: `${dir}/shots/${name}-practice.png`, fullPage: true });
    await p.click('[data-act="mock"]'); await p.waitForTimeout(200);
    for (let i = 0; i < 5; i++) { await p.click('.opt >> nth=1'); await p.click('[data-nextq]'); }
    await p.screenshot({ path: `${dir}/shots/${name}-mock.png`, fullPage: true });
    await p.click('[data-submit] >> nth=0'); await p.waitForTimeout(100); await p.click('.modal [data-really]'); await cm();
    await p.click('[data-review]'); await p.waitForTimeout(200);
    await p.screenshot({ path: `${dir}/shots/${name}-mockres.png` });
    await p.click('[data-home]'); await p.waitForTimeout(100);
    while (await p.$('.modal')) { await p.click('.modal [data-close]'); await p.waitForTimeout(100); }
    await p.click('a[data-tab="practice"]'); await p.click('[data-fc="oop"]'); await p.click('[data-show]'); await p.waitForTimeout(100);
    await p.screenshot({ path: `${dir}/shots/${name}-card.png` });
    await p.click('[data-grade="1"]'); await cm();
    await p.click('[data-quit]'); await p.click('.modal [data-really]');
    await p.click('a[data-tab="me"]'); await p.waitForTimeout(200);
    await p.screenshot({ path: `${dir}/shots/${name}-me.png`, fullPage: true });
    await p.click('a[data-tab="today"]'); await p.waitForTimeout(200);
    await p.screenshot({ path: `${dir}/shots/${name}-today2.png`, fullPage: true });
    const ow = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
    if (ow) errs.push(name + ' HORIZONTAL OVERFLOW');
    await ctx.close();
  }
  console.log(errs.join('\n') || 'no errors');
  await b.close();
})().catch(e => { console.error('TEST FAIL', e); process.exit(1); });
