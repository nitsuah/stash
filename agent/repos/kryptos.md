# KRYPTOS

[![CI fast](https://github.com/nitsuah/kryptos/actions/workflows/ci-fast.yml/badge.svg)](https://github.com/nitsuah/kryptos/actions)

[![CI (smoke)](https://github.com/nitsuah/kryptos/actions/workflows/demo-smoke.yml/badge.svg)](https://github.com/nitsuah/kryptos/actions)

[![CI (slow)](https://github.com/nitsuah/kryptos/actions/workflows/ci-slow.yml/badge.svg)](https://github.com/nitsuah/kryptos/actions)

Inspired by *The Unexplained* with William Shatner, I set out to solve Kryptos using Python! This project focuses on
implementing cryptographic techniques, specifically the Vigenère cipher and structural transposition analysis, to
decrypt the famous Kryptos sculpture.

## TL;DR

This Kryptos repository is a research toolkit for exploring layered cipher hypotheses (Vigenère, Hill, transposition,
masking, and related hybrids) with an emphasis on reproducible pipelines and scoring heuristics.

## docs

All Related documents / quick links can generally be found in `docs/`:

- Phase 6 Roadmap: `docs/PHASE_6_ROADMAP.md`
- Agents Architecture: `docs/reference/AGENTS_ARCHITECTURE.md`
- API Reference: `docs/reference/API_REFERENCE.md`
- Autonomous System: `docs/reference/AUTONOMOUS_SYSTEM.md`
- API Reference: `docs/reference/API_REFERENCE.md`
- Changelog: `docs/CHANGELOG.md`

**K4 is the last unsolved piece of a CIA sculpture puzzle.** Imagine a secret message carved in copper that nobody has
cracked in 30+ years. We're using Python to systematically try every reasonable decryption method – techniques that
crypto analysts may have attempted manually but couldn't exhaustively explore. Our approach combines automated testing
with intelligent scoring to measure how "English-like" each result appears:

1. **Hill Cipher** - Matrix-based substitution where letters become numbers, transform through matrix multiplication,
then convert back.

1. **Transposition** - Systematic letter rearrangement (write in columns, read in rows, or more complex patterns)

1. **Masking** - Identifying and removing dummy letters that serve as padding or obfuscation

1. **Berlin Clock** - Using the iconic clock's binary time pattern as a cryptographic key

1. **Combo Attacks** - Chaining multiple methods together (K4 likely uses 2-3 techniques layered in sequence)

We evaluate candidates using linguistic patterns – common letter pairs, trigram frequencies, real word detection – to
identify promising decryptions. Think of it as trying thousands of lock combinations, but guided by cryptanalytic
intuition rather than brute force. After all, humans design puzzles with intention, not randomness!

## Recent Updates

### Phase 6 Comprehensive Cleanup (October 2025)

**Code Optimization**: Removed **3,554 lines** of unnecessary code while preserving all functionality

- Automated cleanup: -2,877 lines (docstrings, comments, verbose logging) across 65 files
- Deprecated code removal: -677 lines (unused configs, obsolete tests)
- Fixed K3 ciphertext correction (336 chars)

**Test Suite Optimization**: 607 tests total (**583 fast** / 24 slow)

- Added `@pytest.mark.slow` to long-running statistical validation tests
- Fast iteration: `pytest -m "not slow"` runs 583 tests in ~1-2 minutes
- Full validation: `pytest` includes Monte Carlo tests (10+ min) for autonomous solving verification

**Result**: Leaner codebase, faster development cycle, maintained 100% test pass rate

## Current Progress

### ✅ K1: "Between subtle shading and the absence of light lies the nuance of iqlusion"

- **Status**: Solved.
- **Details**: Decrypted via Vigenère using keyed alphabet `KRYPTOSABCDEFGHIJLMNQUVWXZ`. Intentional misspelling preserved: `IQLUSION`.

### ✅ K2: "It was totally invisible. How's that possible?"

- **Status**: Solved.
- **Details**: Vigenère (key: `ABSCISSA`). Includes embedded null/structural padding (`S`) for historical alignment. Contains geospatial coordinates and narrative text.

### ✅ K3: "Slowly, desperately slowly, the remains of passage debris..."

- **Status**: Solved (double rotational transposition method).
- **Details**: Implemented the documented 24×14 grid → 90° rotation → reshape to 8-column grid → second 90° rotation. Resulting plaintext matches known solution including deliberate misspelling `DESPARATLY` (analogous to `IQLUSION` in K1).

### ℹ️ K4: The unsolved mystery

- **Status**: Unsolved.
- **Implemented Toolkit**: See K4 modules below (Hill cipher exploration, scoring, constraint pipeline, multi-stage fusion).
- **Latest Additions**: Multi-crib positional transposition stage, attempt logging & persistence, advanced linguistic metrics, 3x3 Hill key pruning (partial_len/partial_min tunable in hill constraint stage).

## Deliberate Misspellings / Anomalies

| Section | Cipher Plaintext Form | Expected Modern Spelling | Note |
|---------|-----------------------|---------------------------|------|
| K1      | IQLUSION              | ILLUSION                  | Intentional artistic alteration |
| K3      | DESPARATLY            | DESPERATELY               | Preserved from sculpture transcription |

### K2 Structural Padding

K2 contains systematic X (and some Y) insertions serving as alignment/null separators rather than mistakes. They should
be treated as structural artifacts when analyzing pattern continuity or constructing transposition hypotheses.

## Features

- **Vigenère Cipher** with keyed alphabet handling
- **K3 Double Rotational Transposition** implementation
- **Config-driven** (`config/config.json`) for ciphertexts, keys, and parameters
- **Test Suite** validating K1–K3 solutions
- **Frequency, n-gram, and crib-based scoring utilities**
- **Hill cipher (2x2 & 3x3)** encryption/decryption + key solving from crib segments
- **3x3 Hill assembly variants & pruning** (row/col/diagonal constructions + partial score pruning)
- **Constrained Hill key derivation** from `BERLIN` / `CLOCK` cribs (single & pairwise) with caching
- **Modular pipeline architecture** (stage factories for all hypothesis families)
- **Columnar transposition** search (partial-score pruning) and crib-constrained inversion utilities
- **Multi-crib positional transposition stage** (anchors multiple cribs simultaneously)
- **Adaptive transposition search** with sampling prefix caching heuristics
- **Masking/null-removal stage** exploring structural padding elimination variants
- **Berlin Clock shift hypothesis** (full lamp state enumeration + dual-direction application)
- **Weighted multi-stage fusion utilities** for score aggregation
- **High-quality quadgram table** auto-loaded when present (`data/quadgrams_high_quality.tsv`)
- **Advanced linguistic metrics** (wordlist hit rate, trigram entropy, bigram gap variance, entropy, repeating bigram fraction)
- **Memoized scoring** (LRU cache for repeated candidate evaluation)
- **Pipeline profiling** (per-stage duration metadata)
- **Transformation trace & lineage** (each candidate records stage + transformation chain)
- **Attempt logging & persistence** (Hill, Clock, Transposition permutations → timestamped JSON)
- **Candidate reporting artifacts** (JSON + optional CSV summaries)
- **Adaptive fusion weighting** (optional `adaptive=True` in composite run)

## K4 Analysis Toolkit

Located under `kryptos/k4/` (migrated from `src/k4/`):

See `docs/reference/API_REFERENCE.md` for code-level API documentation.

## Roadmap

See `docs/PHASE_6_ROADMAP.md` for current status and next phase objectives.

## CLI Usage Examples

```bash
# List sections
kryptos sections

# Composite K4 decrypt
kryptos k4-decrypt --cipher data/k4_cipher.txt --limit 40 --adaptive --report

# Persist attempt logs
kryptos k4-attempts --label k4

# Tuning: crib weight sweep
kryptos tuning-crib-weight-sweep --weights 0.25,0.5,1.0,1.5 \
  --cribs BERLIN,CLOCK \
  --samples data/holdout_samples.txt --json

# Tuning: pick best weight
kryptos tuning-pick-best --csv artifacts/tuning_runs/run_20251023T120000/crib_weight_sweep.csv
```
