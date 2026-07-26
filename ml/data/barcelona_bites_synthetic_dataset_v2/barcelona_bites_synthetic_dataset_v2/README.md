# Synthetic Supplier Spec-Sheet Dataset v2 — Barcelona Bites
### Rebuilt against every finding in the v1 Data Quality Audit. Every fix below was verified programmatically, not just claimed.

## Headline numbers

| Metric | v1 | v2 | Change |
|---|---|---|---|
| Total documents | 62 | **343** (264 clean + 79 scanned) | 5.5x |
| Table layout — real extractable table structure | **0 tables detected** (fake) | **1 gridded table/doc, verified via `pdfplumber.extract_tables()`** | Fixed |
| Allergen class balance (max/min ratio across 14 EU categories) | 3.3x (sulphites 23 vs soy 7) | **1.0x — exactly 45 "contains" examples per allergen** | Fixed |
| Data leakage (clean/scanned pairs split across train/test) | Confirmed present, unmitigated | **0 — enforced via `pair_id` split-safe grouping, verified** | Fixed |
| Supplier diversity (top supplier's share of dataset) | 22.6% | **6.8%**, 25 unique suppliers (up from 10) | Fixed |
| Unique ingredient phrases (absolute vocabulary size) | 138 | **356** | 2.6x |
| Missing structural metadata (batch, origin, storage, address) | Absent entirely | **Present on every document** | Fixed |
| Mixed-language / bilingual documents | 0 | **42** (dedicated `bilingual` layout) | Fixed |
| Scan degradation range | One fixed setting (±2.5°) | **3 graded tiers: mild / moderate / severe (±2.5° / ±6° / ±15° + 12% upside-down)** | Fixed |
| Independent label verification | Never done — labels and docs shared one source of truth | **264/264 documents independently re-verified by re-parsing rendered PDF text against labels — 100% pass after 2 real bugs found and fixed** | New |
| Train/val/test split | None provided | **70/15/15, pair-aware (leak-proof)** | New |

## What genuinely changed vs. what's still a synthetic-data ceiling

**Fixed, verified, real:**
- The `table` layout now renders an actual bordered grid (`GRID` table style) — `pdfplumber` correctly detects it as a structured table with 12 rows, confirmed by direct extraction test. In v1 this layout was mislabeled; it now does what its name claims.
- Allergen class imbalance is fully closed via a `BalancedAllergenSampler` that always picks the least-used allergen next — every one of the 14 EU Annex II categories now has exactly 45 "contains" examples in the clean set (was up to 3.3x skewed).
- Leakage is structurally impossible now, not just documented as a risk: every clean/scanned pair shares a `pair_id`, and the train/val/test split is computed by grouping on `pair_id` before assignment — verified that zero pair_ids span more than one split.
- Every document now carries batch/lot number, country of origin, storage conditions, supplier address, and net weight — the structural fields v1 was missing entirely.
- A dedicated `bilingual` layout (42 documents) now covers the real-world pattern where the main document is in one language and the allergen declaration footer is in another — explicitly flagged in each record via `allergen_declaration_language`.
- **Independent verification caught and fixed 2 real generator bugs** before you'd ever have seen them in a training run: (1) long ingredient phrases were occasionally line-wrapped mid-phrase in the matrix layout, breaking substring matching — fixed by normalizing whitespace; (2) the "Free from: Milk (including lactose)" declaration text itself contains the word "lactose," which is also a milk trigger phrase — the checker was flagging the category label as if it were a contradictory ingredient mention. Both are now excluded correctly. Final independent pass rate: **264/264 (100%)**, logged in `verification_report.json`.

**Improved but still bounded (be honest about this):**
- Ingredient vocabulary grew from 138 to 356 unique phrases in absolute terms (2.6x), which is real progress — but because document count grew faster (5.5x), the *ratio* of unique-to-total mentions actually went down (26% → 14.4%). More documents drawing from a still-finite pool is expected; if you scale this dataset further, scale the vocabulary in `allergen_data.py` proportionally or the ratio will keep dropping.
- Scan degradation now has 3 real tiers, measured with actual OCR (Tesseract) word-recall: **mild ≈71%, moderate ≈69%, severe ≈0.6%** recall vs. clean text. The severe tier isn't broken — it's intentionally brutal (up to 15° rotation plus a 12% chance of a fully upside-down page) and correctly exposes that naive OCR without a deskew/orientation-correction preprocessing step fails almost completely on this class of document. Treat "severe" as a test of your *preprocessing pipeline*, not your text-recognition model.
- Supplier diversity is better (25 suppliers, max 6.8% share) but every supplier still shares the same six underlying layout templates — real suppliers would each have their own idiosyncratic formatting. This dataset cannot manufacture that; only real documents can.

**What is NOT fixed, and cannot be fixed by generation alone:**
- **This is still a 100% synthetically generated dataset.** Every phrase, layout, and "supplier" originated from the scripts in this package. No amount of internal balancing or verification changes that fact. A model trained and evaluated purely on this data has not been validated against real-world supplier document behavior — inconsistent real-world fonts, actual company letterheads, genuine scanning artifacts from real fax/scan hardware, handwritten annotations, and truly idiosyncratic per-supplier formatting are all still absent.
- **Do not report a headline production accuracy/recall number based on this dataset alone.** Use it to validate your pipeline runs correctly, to catch integration bugs early (as the verification step here already did), and to pressure-test specific failure modes (footnote traces, negation, bilingual declarations, severe scan degradation) — then confirm the real number on real, held-out Barcelona Bites supplier documents before calling anything production-ready.

## Contents

| File / Folder | Contents |
|---|---|
| `pdfs/` | 264 clean synthetic spec-sheet PDFs |
| `pdfs_scanned/` | 79 degraded scans across 3 severity tiers (mild/moderate/severe) |
| `ground_truth.jsonl` | Labels for the 264 clean documents |
| `ground_truth_scanned.jsonl` | Labels for the 79 scanned documents (includes `scan_severity_tier`, `source_clean_file`) |
| `all_ground_truth.jsonl` | **Master file** — all 343 records, includes `split` (train/val/test) and `pair_id` |
| `verification_report.json` | Output of the independent label-verification pass (264/264 pass) |
| `allergen_data.py` | Expanded EU Annex II taxonomy + EN/ES/CA vocabulary (356 unique ingredient phrases, 70 product names, 25 suppliers) |
| `generate_v2.py` | Main generator (balanced sampler, gridded tables, bilingual layout, metadata fields) |
| `make_scanned_subset_v2.py` | Tiered scan-degradation generator |
| `verify_labels.py` | Independent re-verification script — re-run it any time you regenerate or extend the dataset |

## Recommended next step (still true, still important)

Before calling any model trained on this "production-ready": source 15-30 real, anonymized Barcelona Bites supplier PDFs and run them through `verify_labels.py`-style manual review as your true held-out test set. This dataset is now a solid, internally-consistent, leak-free training and pipeline-validation set — it is not, and cannot be, a substitute for that final real-world check.
