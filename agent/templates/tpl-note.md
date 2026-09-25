<%*
// New vault note: pick the hub it belongs under, so it lands in the graph like routine-written notes.
// Links are built as strings so this template itself adds no wikilink to the graph.
const hubs = app.vault.getMarkdownFiles()
  .map(f => f.path.replace(/\.md$/, ""))
  .filter(p => /^repos\/[^/]+$/.test(p) || /^projects\/[^/]+$/.test(p) || p === "VAULT-MAP")
  .sort();
const up = await tp.system.suggester(hubs, hubs, false, "Parent hub (Esc = none)");
if (up) { tR += "---\nup: \"" + "[" + "[" + up + "]" + "]\"\n---\n\n"; }
-%>
# <% tp.file.title %>

> What this note is for, in one line.

