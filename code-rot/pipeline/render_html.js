// Rendert HTML/SVG-Datei als PNG: node render_html.js in.html out.png [w] [h] [scale]
const { chromium } = require('playwright');
(async () => {
  const [,, inp, out, w = '1080', h = '1920', scale = '1'] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +scale });
  await p.goto('file://' + require('path').resolve(inp));
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: out, omitBackground: true });
  await b.close();
})();
