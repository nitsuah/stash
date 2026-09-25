---
kind: repo-hub
repo: kryptos
---

# kryptos

> Reviewed: 2026-09-23 (no material change since 2026-09-16 PMO audit — see [[pmo-audit-2026-09-16]])

## Overview

Python cryptanalysis research toolkit for solving the Kryptos CIA sculpture puzzle. K1, K2, K3 are solved; K4 remains unsolved. Implements Vigenère, Hill cipher, transposition, masking, Berlin Clock, Quagmire I–IV, Beaufort, and composite pipeline attacks with autonomous Q/OPS/SPY agent system, FastAPI dashboard, React SPA, Neon PostgreSQL persistence, and turbovec RAG semantic search.

## Current Goals / Roadmap Focus

Roadmap has advanced well past the Q1 2027 dashboard/API phases previously tracked here — those are now Phases 1–5 (all ✅) in `docs/ROADMAP.md`, superseded by a "Physical/Geometric Pivot" (Phases 6–8):

Phases 1–5 (foundational attacks, dashboard, API, validation, K1–K3 tooling): ✅ all complete.

Phase 6 — Physical/Geometric Pivot: ✅ Complete (2026-09-01). 13 of 15 code-executable research-brief items implemented and run against real K4 — 24-column geometric permutation front-end, precise WGS84 geodesy (Mengenlehreuhr→Weltzeituhr bearing), Nov 9 1989 Berlin Wall clock state, Myszkowski/Trifid ciphers, SA substitution search, P2/P5/P6 executed for real for the first time. All null (2.6M+ candidates across Phases 6–7).

Phase 7 — Shape-changing transposition + solar-geometry "shadow of the word" hypothesis: ✅ Complete (2026-09-01). World Clock city-list keyword source grown to 130/146 confirmed names; cross-vector consensus scoring built; scheduled overnight sweep runner built. All null.

Phase 8 — Primary-source sourcing (active, opened 2026-09-01): of three sourcing gaps, two are closed (World Clock segment photos, sub-minute Berlin Wall timestamp) — one remains open:
- [ ] Source the Kryptos compass rose's actual measured bearing (needs FOIA/Elonka Dunin outreach — human action, not code)

Multiple follow-on external-review passes (2026-09-02/03) closed a real bug (`keystream_validator.K4_CRIBS` off-by-one on EAST/NORTHEAST positions), added `plaintext_evidence`, extended known-plaintext inversion to rectangular grids, tested the CIA-confirmed "read from the back" tableau reading, and ran newly-discovered classical ciphers (Playfair/Four-Square/Bifid/Autokey) and K0 Morse-slab keywords for the first time — all null.

Phase 5 (Post-solution, standing, blocked on K4 being solved):
- [ ] Solution documentation — full attack path, key insights, narrative
- [ ] README update reflecting solution

## Open P0/P1 Tasks

Kryptos's TASKS.md doesn't use P0/P1 labels; below are the only genuinely-open items in `docs/TASKS.md`'s Active section (both blocked on a human, not code):

- [ ] **Source the Kryptos compass rose's actual measured bearing** — FOIA request to CIA or direct outreach to Elonka Dunin, both drafted and ready to send. Flagged "[You — the only send]" — needs the repo owner to actually send it.
- [ ] **Ask CIA Public Affairs whether an authorized research visit exists** — outreach draft ready, also flagged "[You — the only send]".

Everything else (Phases 1–8's code work) is done. No open engineering P0/P1s.

## Blockers

- K4 remains unsolved — every code-derivable attack vector tried across Phases 1–8 has returned null (single-layer, 2-layer, 3-layer composite, full Physical/Geometric Pivot, shape-changing transposition, classical ciphers, solar/geodesy hypotheses).
- What's left needs new source material, not new code: the Kryptos compass rose's exact measured bearing is still unknown community-wide (per elonka.com's own wishlist) — the two open Active tasks above are blocked on outreach responses (FOIA / Elonka / CIA Public Affairs), not on engineering.
- If outreach doesn't surface new material, Phase 8 is explicitly "paused" — the team does not expect more sweep variants over the same structural assumptions to move this forward (cross-vector consensus scan found zero agreement across 30 null-result artifacts).

## Recent Changes (Unreleased)

Root `CHANGELOG.md` [Unreleased] is stale (RAG/serve additions only); `docs/ROADMAP.md`/`docs/TASKS.md` (dated 2026-09-03) show much more recent activity:

- **Phase 6 (2026-08-29 to 2026-09-01)**: Physical/Geometric Pivot — 24-column geometric permutation front-end, precise WGS84 geodesy module (`kryptos.k4.geodesy`), Mengenlehreuhr→Weltzeituhr bearing, Nov 9 1989 Berlin Wall clock state, Myszkowski transposition, Trifid cipher, SA substitution search behind the geometric front-end, dashboard Pivot Status panel. All null.
- **Phase 7 (2026-09-01)**: shape-changing transpose family wired into the geometric sweep; `kryptos.k4.solar_geometry` (World Clock topper rotation + real solar position at CIA HQ); World Clock city list grown 9→130/146 confirmed names; `kryptos.k4.cross_vector_consensus`; scheduled overnight sweep runner. All null.
- **Phase 8 (2026-09-01 onward)**: two of three primary-source gaps closed (World Clock segment photos via more Wikimedia Commons images; sub-minute Nov 9 1989 timestamp via `chronik-der-mauer.de`'s Hertle transcript); compass-rose bearing remains open.
- **2026-09-02/03 external-review follow-ups**: found and fixed a real bug — `keystream_validator.K4_CRIBS` had EAST/NORTHEAST cribs one position too high since introduction (also duplicated in `key_csp.py`/`clock_hill_attack.py`); built `plaintext_evidence` (confidence-tiered crib data), `known_plaintext_inversion` (extended to rectangular grids, 3.67M permutations tested), `classical_cipher_sweep` (Playfair/Four-Square/Bifid/Autokey — never previously run against real K4), `k0_morse_keywords` (from the sculpture's Morse-code entrance slabs, never used before); consolidated 17 duplicate K4-ciphertext literals to one canonical import. All new attacks null.
- Test suite grown to 1271 test functions / 1192 fast-collected (0 failures, 28 skipped), 89.35% coverage as of 2026-08-22 (`docs/METRICS.md`), up from 633/95% at the prior review.

## 2026-09-16 PMO Audit

`docs/TASKS.md`/`docs/ROADMAP.md` re-checked line-by-line — still accurate, no contradictions (this repo already self-flags its own doc staleness inline, e.g. ROADMAP's Phase 3 note). Real bug found and fixed: README's "Docker Fast Coverage" command was missing `geographiclib` from its manual pip-install list, breaking collection of 5 K4 geometry/geodesy test modules (`ModuleNotFoundError`) — that dependency has been real since the Phase 6 geodesy work but the doc snippet was never updated. Fixed, then re-ran the corrected command for real numbers: **1658 passed, 34 skipped, 26 deselected (slow)** in 261.37s, **89.27% coverage** (was 1192/28/89.35% on 2026-08-22 — test count jumped ~40% from the Phase 6-8 work, coverage % stayed essentially flat). `docs/METRICS.md` refreshed accordingly. `docs/ROADMAP.md`'s "Next Review: 2026-09-15" is now 1 day overdue — left untouched (content is accurate) but flagged for next cycle. PR: [nitsuah/kryptos#215](https://github.com/nitsuah/kryptos/pull/215).

## Verified Runbook (PMO 2026-09-24)

> Commands verified during the 2026-09-24 PMO audit (`agent/reports/pmo-audit-2026-09-24.md` §7). **obn-review: keep this section when refreshing the summary.**

- The backend runs on Render's free plan (`kryptos-kg8t.onrender.com`), and the first request cold-starts in about 20s. Allow for this in live checks. The frontend is on Netlify.

<!-- vault-links:start -->
## Vault links

_Generated by `scripts/build-vault-indexes.py`; edits inside this block are overwritten._

- Docs: [[repos/kryptos/README|README]] (every doc hangs off its Docs Index)
- Overview: [[projects/KB/kryptos-overview|KB overview]]
- Latest LOC report: [[reports/eng-loc-kryptos-2026-09-01|2026-09-01]] (older ones chain from it)
- Latest MINI report: [[reports/eng-mini-kryptos-2026-09-01|2026-09-01]] (older ones chain from it)
<!-- vault-links:end -->
