// Quick checks for The Bowl site. Run: python3 -m http.server 8765 & node tools/check.js
const { chromium } = require('playwright');
const BASE = process.env.BASE || 'http://localhost:8765/';
const SHOTS = process.env.SHOTS || '';
let pass = 0, fail = 0;
const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL:', m); } };
(async () => {
  const b = await chromium.launch();
  for (const vp of [{ width: 1280, height: 800, n: 'desktop' }, { width: 375, height: 740, n: 'phone' }, { width: 320, height: 640, n: 'small' }]) {
    const p = await b.newPage({ viewport: { width: vp.width, height: vp.height } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    const bad404 = []; p.on('response', r => { if (r.status() >= 400 && r.url().startsWith(BASE)) bad404.push(r.url()); });
    await p.goto(BASE, { waitUntil: 'load' }); await p.waitForTimeout(800);
    ok(errs.length === 0, vp.n + ' page errors: ' + errs.join('; '));
    ok(bad404.length === 0, vp.n + ' missing files: ' + bad404.join(', '));
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    ok(sw <= vp.width, `${vp.n} horizontal scroll ${sw} > ${vp.width}`);
    ok(await p.$('meta[name=robots][content*=noindex]') !== null, 'noindex missing');
    const bad = await p.evaluate(() => [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.querySelector(h)));
    ok(bad.length === 0, 'broken in-page links: ' + bad);
    const small = await p.evaluate(() => [...document.querySelectorAll('.btn,.chips a')].filter(e => e.offsetParent && e.getBoundingClientRect().height < 42).length);
    ok(small === 0, vp.n + ' small tap targets: ' + small);
    ok(await p.$$eval('a[href^="tel:"]', a => a.length > 0 && a.every(x => x.getAttribute('href') === 'tel:+17707021129')), 'tel links');
    ok(await p.$$eval('a[target=_blank]', a => a.every(x => x.rel.includes('noopener'))), 'noopener');
    ok(await p.$$eval('img', a => a.every(x => x.hasAttribute('alt'))), 'img alt');
    const broken = await p.evaluate(async () => { const r=[]; for (const i of document.querySelectorAll('img')) { i.loading='eager'; try { await i.decode(); } catch(e) { r.push(i.src); } } return r; });
    ok(broken.length === 0, 'broken images: ' + broken);
    ok((await p.locator('#status').textContent()) !== '', 'status text');
    const txt = await p.evaluate(() => document.body.innerText);
    ok(!/Falafel|429-8999|950 Cobb|halal/i.test(txt), 'leftover Falafel Cafe text');
    if (SHOTS && vp.n !== 'small') await p.screenshot({ path: `${SHOTS}/shot-${vp.n}.png`, fullPage: true });
    await p.close();
  }
  // Open/closed logic at fixed Eastern times. Hours: Mon/Wed/Thu 11-9, Tue closed, Fri/Sat 11-10, Sun 11-8.
  const cases = [
    ['2026-11-24T12:00:00', /^Closed Tuesdays\. Opens tomorrow at 11 am$/, 'Tuesday, closed'],
    ['2026-11-23T10:00:00', /^Closed now\. Opens today at 11 am$/, 'Monday, 11 am to 9 pm'],
    ['2026-11-23T13:00:00', /^Open now, until 9 pm$/, null],
    ['2026-11-23T21:30:00', /^Closed now\. Opens Wednesday at 11 am$/, null],
    ['2026-11-28T21:45:00', /^Open now, until 10 pm$/, null],
    ['2026-11-22T19:59:00', /^Open now, until 8 pm$/, 'Sunday, 11 am to 8 pm'],
    ['2026-11-27T22:30:00', /^Closed now\. Opens tomorrow at 11 am$/, null],
  ];
  for (const [t, re, today] of cases) {
    const p = await b.newPage();
    await p.addInitScript(`window.__NOW=${JSON.stringify(t)}`);
    await p.goto(BASE, { waitUntil: 'domcontentloaded' });
    const s = await p.locator('#status').textContent();
    ok(re.test(s), `status at ${t}: "${s}"`);
    if (today) { const d = await p.locator('#today').textContent(); ok(d === today, `today at ${t}: "${d}"`); }
    await p.close();
  }
  // Legal page
  const p = await b.newPage(); await p.goto(BASE + 'legal.html');
  const lt = await p.evaluate(() => document.body.innerText);
  ok(!/Falafel|429-8999|950 Cobb|hummus|tahini/i.test(lt), 'legal leftovers');
  for (const id of ['privacy','terms','accessibility','allergens','credits']) ok(await p.$('#'+id) !== null, 'legal section ' + id);
  ok(await p.$('meta[name=robots][content*=noindex]') !== null, 'legal noindex');
  await b.close();
  console.log(`${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
})();
