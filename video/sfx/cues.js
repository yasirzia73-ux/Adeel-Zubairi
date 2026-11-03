const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const out = {};
  for (const [k, f] of [['v1', '/home/user/Adeel-Zubairi/video/maya-jake/animation.html'], ['v2', '/home/user/Adeel-Zubairi/video/year-end-checklist/animation.html'], ['v3', '/home/user/Adeel-Zubairi/video/401k-explained/animation.html'], ['v4', '/home/user/Adeel-Zubairi/video/binance-hack/animation.html'], ['v5', '/home/user/Adeel-Zubairi/video/iran-war-cost/animation.html']]) {
    await p.goto('file://' + f);
    out[k] = await p.evaluate('({cues: CUE_LIST(), scenes: SCENES, order: ORDER, total: TOTAL})');
  }
  fs.writeFileSync('/tmp/sfx/timing.json', JSON.stringify(out)); await b.close();
})();
