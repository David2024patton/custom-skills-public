#!/usr/bin/env bash
# Browser visual check: boot the app, screenshot routes. Requires Node + Playwright.
# Usage: browser-check.sh <base-url> [report-dir]
set -u
BASE="${1:?usage: browser-check.sh <base-url> [report-dir]}"
DIR="${2:-ui-report}"
mkdir -p "$DIR"
echo "=== UI visual check: $BASE -> $DIR ==="
command -v node >/dev/null 2>&1 || { echo "SKIP: node not installed"; exit 0; }
node -e "require.resolve('playwright')" >/dev/null 2>&1 || {
  echo "Playwright not found. Install: npm i -D playwright && npx playwright install chromium"; exit 0; }
cat > "$DIR/_shot.js" <<'EOF'
const { chromium } = require('playwright');
(async () => {
  const base = process.argv[2], dir = process.argv[3];
  const routes = process.argv[4] ? process.argv[4].split(',') : ['/'];
  const widths = { desktop: 1280, tablet: 768, phone: 375 };
  const browser = await chromium.launch();
  const errors = [];
  for (const [name, w] of Object.entries(widths)) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
    const page = await ctx.newPage();
    page.on('console', m => { if (m.type() === 'error') errors.push(name + ' console: ' + m.text()); });
    page.on('requestfailed', r => errors.push(name + ' reqfail: ' + r.url()));
    for (const route of routes) {
      try {
        await page.goto(base + route, { waitUntil: 'networkidle', timeout: 20000 });
        await page.screenshot({ path: dir + '/' + name + route.replace(/[^a-z0-9]/gi, '_') + '.png', fullPage: true });
        console.log('SHOT', name, route);
      } catch (e) { console.log('ERROR', name, route, e.message); errors.push(name + ' ' + route + ': ' + e.message); }
    }
    await ctx.close();
  }
  await browser.close();
  require('fs').writeFileSync(dir + '/console-errors.txt', errors.join('\n') || '(none)');
  console.log('Wrote', errors.length, 'errors to console-errors.txt');
})();
EOF
node "$DIR/_shot.js" "$BASE" "$DIR" "${ROUTES:-/}" 
echo "Screenshots and console-errors.txt in $DIR. Attach to the report for David's sign-off."
