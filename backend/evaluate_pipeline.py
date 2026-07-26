import json
import os
import sys
import time

sys.path.append(os.getcwd())

from app.mineru_service import run_mineru_extraction
from app.allergen_service import detect_allergens

# Paths
DATASET_DIR = r"C:\barcelona-bites-allergen-ai\ml\data\barcelona_bites_synthetic_dataset_v2\barcelona_bites_synthetic_dataset_v2"
PDFS_DIR = os.path.join(DATASET_DIR, "pdfs")
GROUND_TRUTH_PATH = os.path.join(DATASET_DIR, "ground_truth.jsonl")

SAMPLE_SIZE_PER_TEMPLATE = 2

# ---- Allergen name normalization ----
# Maps any variant spelling/naming to one canonical name, so "soy" and "soybeans"
# are correctly recognized as the same allergen instead of counted as a mismatch.
ALLERGEN_ALIASES = {
    "soy": "soybeans",
    "soybeans": "soybeans",
    "soja": "soybeans",
    "nuts": "tree nuts",
    "tree nuts": "tree nuts",
    "gluten": "cereals containing gluten",
    "cereals containing gluten": "cereals containing gluten",
    "sulphites": "sulphur dioxide/sulphites",
    "sulphur dioxide/sulphites": "sulphur dioxide/sulphites",
    "sulphur dioxide and sulphites": "sulphur dioxide/sulphites",
    "milk": "milk",
    "eggs": "eggs",
    "egg": "eggs",
    "peanuts": "peanuts",
    "crustaceans": "crustaceans",
    "fish": "fish",
    "molluscs": "molluscs",
    "celery": "celery",
    "mustard": "mustard",
    "sesame": "sesame",
    "lupin": "lupin",
}


def normalize_allergen(name: str) -> str:
    key = name.strip().lower()
    return ALLERGEN_ALIASES.get(key, key)  # fall back to the lowercased name if not in the map


# ---- Retry wrapper for rate-limited API calls ----
def detect_allergens_with_retry(extracted_text, max_retries=3, delay_seconds=15):
    for attempt in range(1, max_retries + 1):
        try:
            return detect_allergens(extracted_text)
        except Exception as e:
            if attempt == max_retries:
                raise
            print(f"    Retry {attempt}/{max_retries} after error: {e}")
            time.sleep(delay_seconds)


# 1. Load ground truth
ground_truth_entries = []
with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as f:
    for line in f:
        ground_truth_entries.append(json.loads(line))

print(f"Total ground truth entries loaded: {len(ground_truth_entries)}")

# 2. Build a stratified sample
from collections import defaultdict

by_template = defaultdict(list)
for entry in ground_truth_entries:
    by_template[entry["layout_template"]].append(entry)

sample = []
for template, entries in by_template.items():
    sample.extend(entries[:SAMPLE_SIZE_PER_TEMPLATE])

print(f"Sample size: {len(sample)} PDFs across {len(by_template)} templates")

# 3. Run the pipeline on each sampled PDF and compare to ground truth
results = []

for entry in sample:
    pdf_filename = entry["file"]
    pdf_path = os.path.join(PDFS_DIR, pdf_filename)

    expected_allergens = set(normalize_allergen(a) for a in entry["allergens_all_eu_annex_ii"])

    print(f"\nProcessing: {pdf_filename} ...")

    try:
        extracted_text = run_mineru_extraction(pdf_path)
        prediction = detect_allergens_with_retry(extracted_text)

        predicted_allergens = set(
            normalize_allergen(a["allergen"]) for a in prediction.get("allergens_detected", [])
        )

        missed_allergens = expected_allergens - predicted_allergens
        extra_allergens = predicted_allergens - expected_allergens

        results.append({
            "file": pdf_filename,
            "expected": sorted(expected_allergens),
            "predicted": sorted(predicted_allergens),
            "missed": sorted(missed_allergens),
            "extra": sorted(extra_allergens),
            "status": "ok",
        })

        print(f"  Expected: {sorted(expected_allergens)}")
        print(f"  Predicted: {sorted(predicted_allergens)}")
        if missed_allergens:
            print(f"  ⚠️ MISSED (false negative): {sorted(missed_allergens)}")
        if extra_allergens:
            print(f"  ℹ️ Extra (false positive): {sorted(extra_allergens)}")
        if not missed_allergens and not extra_allergens:
            print(f"  ✅ Perfect match")

    except Exception as e:
        results.append({"file": pdf_filename, "status": "error", "error": str(e)})
        print(f"  ❌ ERROR (after retries): {e}")

# 4. Save full results
with open("evaluation_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# 5. Print an overall summary
successful = [r for r in results if r["status"] == "ok"]
failed = [r for r in results if r["status"] == "error"]
perfect_matches = [r for r in successful if not r["missed"] and not r["extra"]]
with_real_misses = [r for r in successful if r["missed"]]

print("\n\n===== SUMMARY =====")
print(f"Total PDFs attempted: {len(results)}")
print(f"Successful: {len(successful)}  |  Failed (API errors): {len(failed)}")
print(f"Perfect matches: {len(perfect_matches)}")
print(f"PDFs with at least one missed allergen: {len(with_real_misses)}")
for r in with_real_misses:
    print(f"  - {r['file']}: missed {r['missed']}")

print("\n✅ Evaluation complete. Full results saved to evaluation_results.json")