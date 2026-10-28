<%*
// Decision record: one decision per note, named <topic>-decision so the graph label says what it is.
const hubs = app.vault.getMarkdownFiles()
  .map(f => f.path.replace(/\.md$/, ""))
  .filter(p => /^repos\/[^/]+$/.test(p) || /^projects\/[^/]+$/.test(p))
  .sort();
const up = await tp.system.suggester(hubs, hubs, false, "Repo or project this decision belongs to");
if (up) { tR += "---\nup: \"" + "[" + "[" + up + "]" + "]\"\nkind: decision\nstatus: proposed\n---\n\n"; }
-%>
# <% tp.file.title %>

**Date:** <% tp.date.now("YYYY-MM-DD") %> · **Status:** proposed

## Context

## Decision

## Consequences

