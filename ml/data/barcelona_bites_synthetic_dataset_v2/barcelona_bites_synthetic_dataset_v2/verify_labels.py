import json, pdfplumber, os, sys
from allergen_data import ALLERGENS

OUT_DIR = "/home/claude/synth_dataset_v2"
PDF_DIR = os.path.join(OUT_DIR, "pdfs")

def extract_text(fname):
    with pdfplumber.open(os.path.join(PDF_DIR, fname)) as pdf:
        return " ".join((p.extract_text() or "") for p in pdf.pages).lower()

import re
def normalize(s):
    s = s.lower().replace("ó","o").replace("í","i").replace("á","a").replace("é","e").replace("ú","u").replace("·","")
    s = re.sub(r"\s+", " ", s)  # collapse newlines/wrapped-line breaks so multi-word phrases still match
    return s

FREE_FROM_MARKERS = ["free from", "libre de", "lliure de"]

def strip_free_from_clause(text):
    """Remove the 'Free from: X, Y, Z' sentence itself before checking for trigger-word contradictions,
    since the allergen category name (e.g. 'Milk (including lactose)') can itself contain a trigger
    substring like 'lactose' - that's a label, not an ingredient use, and must not be flagged."""
    for marker in FREE_FROM_MARKERS:
        idx = text.find(marker)
        if idx != -1:
            return text[:idx]
    return text

def verify():
    clean = [json.loads(l) for l in open(os.path.join(OUT_DIR, "ground_truth.jsonl"))]
    results = {"total": len(clean), "pass": 0, "fail": 0, "failures": []}

    for rec in clean:
        text = normalize(extract_text(rec["file"]))
        lang = rec["language"] if rec["layout_template"] != "bilingual" else rec.get("allergen_declaration_language", rec["language"])
        problems = []

        # 1. every "contains" allergen's ingredient trigger phrase used should appear somewhere in the doc text
        for key in rec["allergens_contains"]:
            allergen_name = normalize(ALLERGENS[key][rec["language"]])
            # the ingredient trigger itself is in rec["ingredients"], check at least one word of it is present
            found_ingredient = any(normalize(ing) in text for ing in rec["ingredients"]
                                    if ing in ALLERGENS[key]["triggers"][rec["language"]])
            found_allergen_name = allergen_name in text
            if not (found_ingredient or found_allergen_name):
                problems.append(f"MISSING_CONTAINS_EVIDENCE:{key}")

        # 2. free_from allergens should NOT have their trigger ingredient present in the doc
        #    (checked against text with the "Free from: ..." clause itself stripped out first,
        #     since the category label can innocently contain a trigger word, e.g. "lactose" in
        #     "Milk (including lactose)")
        if "allergens_explicitly_free_from" in rec:
            text_wo_freefrom_clause = strip_free_from_clause(text)
            for key in rec["allergens_explicitly_free_from"]:
                trigger_present = any(normalize(t) in text_wo_freefrom_clause for t in ALLERGENS[key]["triggers"][rec["language"]])
                if trigger_present:
                    problems.append(f"FREE_FROM_CONTRADICTION:{key}")

        # 3. contains/traces overlap check
        if set(rec["allergens_contains"]) & set(rec["allergens_may_contain_traces"]):
            problems.append("CONTAINS_TRACES_OVERLAP")

        if problems:
            results["fail"] += 1
            results["failures"].append({"file": rec["file"], "problems": problems})
        else:
            results["pass"] += 1

    with open(os.path.join(OUT_DIR, "verification_report.json"), "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Verified {results['total']} documents: {results['pass']} PASS / {results['fail']} FAIL")
    if results["failures"]:
        print("Sample failures:")
        for f_ in results["failures"][:10]:
            print(" ", f_)
    return results

if __name__ == "__main__":
    verify()
