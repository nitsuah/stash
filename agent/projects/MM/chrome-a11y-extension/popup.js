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
    await chrome.scripting.executeScript({ target: { tabId: tab.id, allFrames: true }, files: ['axe.min.js'] });
    const frameResults = await chrome.scripting.executeScript({
      target: { tabId: tab.id, allFrames: true },
      func: async () => {
        const r = await window.axe.run(document, { iframes: false, runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } });
        const map = v => ({ id: v.id, impact: v.impact, help: v.help, url: v.helpUrl, count: v.nodes.length, first: v.nodes[0] ? v.nodes[0].target.join(' ') : '', frame: location.href });
        return { violations: r.violations.map(map), incomplete: r.incomplete.map(map) };
      },
    });
    const result = frameResults.flatMap(({ result }) => result?.violations || []);
    const incomplete = frameResults.flatMap(({ result }) => result?.incomplete || []);
    const penalty = result.reduce((s, v) => s + (WEIGHT[v.impact] || 0), 0);
    const box = el('div');
    box.append(el('div', `Score ${Math.max(0, 100 - penalty)} / 100`, ''), el('p', `${result.length} rule${result.length === 1 ? '' : 's'} failed · ${frameResults.length} frame(s) scanned`, 'muted'));
    box.firstChild.id = 'score';
    box.children[1].id = 'violations-count';
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
    if (incomplete.length) {
      const review = el('section');
      review.append(el('h2', `Needs manual review (${incomplete.length})`));
      const reviewList = el('ul');
      for (const item of incomplete) {
        const li = el('li');
        li.append(el('strong', item.help), el('div', `${item.count} element(s) · ${item.frame}`, 'muted'));
        reviewList.append(li);
      }
      review.append(reviewList);
      box.append(review);
    }
    out.replaceChildren(box);
  } catch (err) {
    const error = el('p', `Could not check this page: ${err.message}`); error.id = 'error'; out.replaceChildren(error);
  }
}

document.getElementById('run').addEventListener('click', run);
