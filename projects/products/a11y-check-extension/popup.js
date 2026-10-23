const WEIGHT = { critical: 10, serious: 5, moderate: 2, minor: 1 };
const out = document.getElementById('out');

function el(tag, text, cls) {
  const e = document.createElement(tag);
  if (text !== undefined) e.textContent = text;
  if (cls) e.className = cls;
  return e;
}

async function targetTab() {
  // ?tab=<id> lets automated tests aim the popup at a specific tab; real use falls through to the active tab.
  const forced = new URLSearchParams(location.search).get('tab');
  if (forced) return { id: Number(forced) };
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

async function run() {
  out.replaceChildren(el('p', 'Checking...'));
  try {
    const tab = await targetTab();
    // Audit every frame we are allowed into: axe only sees the document it is loaded in, so iframes need their own run.
    const target = { tabId: tab.id, allFrames: true };
    await chrome.scripting.executeScript({ target, files: ['axe.min.js'] });
    const frames = await chrome.scripting.executeScript({
      target,
      func: async () => {
        if (!window.axe) return null;
        const r = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } });
        return r.violations.map((v) => ({ id: v.id, impact: v.impact, help: v.help, url: v.helpUrl, count: v.nodes.length, first: v.nodes[0] ? v.nodes[0].target.join(' ') : '' }));
      },
    });
    const audited = frames.filter((f) => Array.isArray(f.result));
    const byRule = new Map();
    for (const v of audited.flatMap((f) => f.result)) {
      const seen = byRule.get(v.id);
      if (seen) seen.count += v.count;
      else byRule.set(v.id, { ...v });
    }
    const result = [...byRule.values()];
    const skipped = frames.length - audited.length;
    const penalty = result.reduce((s, v) => s + (WEIGHT[v.impact] || 0), 0);
    const box = el('div');
    box.append(el('div', `Score ${Math.max(0, 100 - penalty)} / 100`, ''), el('p', `${result.length} rule${result.length === 1 ? '' : 's'} failed, ${audited.length} frame${audited.length === 1 ? '' : 's'} checked${skipped ? `, ${skipped} could not be checked` : ''}`, 'muted'));
    box.firstChild.id = 'score';
    const list = el('ul');
    for (const v of result.sort((a, b) => (WEIGHT[b.impact] || 0) - (WEIGHT[a.impact] || 0))) {
      const li = el('li');
      const link = el('a', v.help);
      link.href = v.url;
      link.target = '_blank';
      link.rel = 'noreferrer';
      li.append(el('span', `${v.impact}: `, v.impact), link, el('div', `${v.count} element${v.count === 1 ? '' : 's'}, first: `, 'muted'));
      li.lastChild.append(el('code', v.first));
      list.append(li);
    }
    box.append(list);
    out.replaceChildren(box);
  } catch (err) {
    out.replaceChildren(el('p', `Could not check this page: ${err.message}`));
  }
}

document.getElementById('run').addEventListener('click', run);
