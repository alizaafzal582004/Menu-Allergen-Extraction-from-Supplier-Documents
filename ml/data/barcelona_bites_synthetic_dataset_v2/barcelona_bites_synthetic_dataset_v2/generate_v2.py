import os, json, random, textwrap, collections, hashlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer
from allergen_data import (ALLERGENS, NEUTRAL_INGREDIENTS, PRODUCT_NAMES, SUPPLIER_NAMES,
                            LABELS_TEXT, COUNTRIES_OF_ORIGIN, STORAGE_CONDITIONS, CITY_ADDRESSES)

random.seed(1234)

OUT_DIR = "/home/claude/synth_dataset_v2"
PDF_DIR = os.path.join(OUT_DIR, "pdfs")
os.makedirs(PDF_DIR, exist_ok=True)

ALLERGEN_KEYS = list(ALLERGENS.keys())
LANGS = ["en", "es", "ca"]

# ---------------- Stratified allergen sampler ----------------
class BalancedAllergenSampler:
    """Ensures every EU Annex II allergen gets picked a roughly similar number of times
    as a 'contains' allergen across the whole generation run (fixes v1's 3.3x class imbalance)."""
    def __init__(self, keys):
        self.keys = keys
        self.counts = collections.Counter({k: 0 for k in keys})

    def pick(self, n):
        # weight = inverse of current count (least-used allergens get picked first)
        weighted = sorted(self.keys, key=lambda k: (self.counts[k], random.random()))
        chosen = weighted[:n]
        for k in chosen:
            self.counts[k] += 1
        random.shuffle(chosen)
        return chosen

SAMPLER = BalancedAllergenSampler(ALLERGEN_KEYS)

def pick_allergens(min_n=1, max_n=4):
    n = random.randint(min_n, max_n)
    return SAMPLER.pick(n)

def build_ingredient_list(lang, contains_keys, n_neutral=7):
    items = []
    for k in contains_keys:
        trigger = random.choice(ALLERGENS[k]["triggers"][lang])
        items.append(trigger)
    neutrals = random.sample(NEUTRAL_INGREDIENTS[lang], min(n_neutral, len(NEUTRAL_INGREDIENTS[lang])))
    items.extend(neutrals)
    random.shuffle(items)
    return items

def batch_id():
    return f"L{random.randint(2026010,2026366)}-{random.randint(100,999)}"

def gt_record(fname, lang, layout, product, supplier, contains_keys, traces_keys, ingredients, meta, pair_id):
    return {
        "file": fname,
        "pair_id": pair_id,
        "language": lang,
        "layout_template": layout,
        "product_name": product,
        "supplier_name": supplier,
        "supplier_metadata": meta,
        "ingredients": ingredients,
        "allergens_contains": sorted(contains_keys),
        "allergens_may_contain_traces": sorted(traces_keys),
        "allergens_all_eu_annex_ii": sorted(list(set(contains_keys) | set(traces_keys))),
    }

def make_meta(lang):
    return {
        "batch_lot_number": batch_id(),
        "country_of_origin": random.choice(COUNTRIES_OF_ORIGIN[lang]),
        "storage_conditions": random.choice(STORAGE_CONDITIONS[lang]),
        "supplier_address": random.choice(CITY_ADDRESSES),
        "net_weight": f"{random.choice([500,1000,2500,5000,10000])} g",
    }

def meta_rows(lang, meta):
    L = LABELS_TEXT[lang]
    return [
        [f"{L['batch']}:", meta["batch_lot_number"]],
        [f"{L['origin']}:", meta["country_of_origin"]],
        [f"{L['storage']}:", meta["storage_conditions"]],
        [f"{L['net_weight']}:", meta["net_weight"]],
        [f"{L['address']}:", meta["supplier_address"]],
    ]

# ---------- Layout 1: TABLE with real gridlines (fixes v1 Major Problem #2) ----------
def layout_table(idx, lang, contains_keys, traces_keys):
    L = LABELS_TEXT[lang]
    product = random.choice(PRODUCT_NAMES[lang])
    supplier = random.choice(SUPPLIER_NAMES)
    meta = make_meta(lang)
    ingredients = build_ingredient_list(lang, contains_keys)
    pair_id = f"doc_{idx:04d}"
    fname = f"{idx:04d}_table_{lang}.pdf"
    path = os.path.join(PDF_DIR, fname)

    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=18*mm, bottomMargin=18*mm,
                             leftMargin=18*mm, rightMargin=18*mm)
    styles = getSampleStyleSheet()
    story = [Paragraph(f"<b>{L['spec_sheet']}</b>", styles["Title"]), Spacer(1, 4)]

    header = [[f"{L['supplier']}:", supplier], [f"{L['product']}:", product],
              [f"{L['code']}:", f"SKU-{random.randint(10000,99999)}"],
              [f"{L['date']}:", f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/2026"]] + meta_rows(lang, meta)
    ht = Table(header, colWidths=[42*mm, 118*mm])
    ht.setStyle(TableStyle([("FONTSIZE",(0,0),(-1,-1),8.5), ("BOTTOMPADDING",(0,0),(-1,-1),3),
                             ("TEXTCOLOR",(0,0),(0,-1), colors.HexColor("#333333"))]))
    story += [ht, Spacer(1, 8), Paragraph(f"<b>{L['ingredients']}</b>", styles["Heading2"])]

    # REAL gridded ingredient table: ingredient | approx % | allergen flag column
    rows = [["#", L["ingredients"], "%"]]
    remaining_pct = 100
    for i, ing in enumerate(ingredients):
        pct = max(1, remaining_pct // (len(ingredients) - i) - random.randint(0, 2))
        remaining_pct -= pct
        rows.append([str(i+1), ing, f"{pct}%"])
    it = Table(rows, colWidths=[10*mm, 120*mm, 20*mm])
    it.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.6, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e0e0e0")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story += [it, Spacer(1, 10), Paragraph(f"<b>{L['allergen_section']}</b>", styles["Heading2"])]
    if contains_keys:
        names = ", ".join(ALLERGENS[k][lang] for k in contains_keys)
        story.append(Paragraph(f"<b>{L['contains']}:</b> {names}.", styles["Normal"]))
    else:
        story.append(Paragraph(L["none_declared"] + ".", styles["Normal"]))
    if traces_keys:
        names = ", ".join(ALLERGENS[k][lang] for k in traces_keys)
        story.append(Paragraph(f"<i>{L['may_contain']}: {names}.</i>", styles["Normal"]))
    doc.build(story)
    return gt_record(fname, lang, "table", product, supplier, contains_keys, traces_keys, ingredients, meta, pair_id)

# ---------- Layout 2: MATRIX ----------
def layout_matrix(idx, lang, contains_keys, traces_keys):
    L = LABELS_TEXT[lang]
    product = random.choice(PRODUCT_NAMES[lang])
    supplier = random.choice(SUPPLIER_NAMES)
    meta = make_meta(lang)
    ingredients = build_ingredient_list(lang, contains_keys)
    pair_id = f"doc_{idx:04d}"
    fname = f"{idx:04d}_matrix_{lang}.pdf"
    path = os.path.join(PDF_DIR, fname)

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 25*mm
    c.setFont("Helvetica-Bold", 14); c.drawString(18*mm, y, L["spec_sheet"]); y -= 9*mm
    c.setFont("Helvetica", 9)
    for line in [f"{L['product']}: {product}", f"{L['supplier']}: {supplier}",
                 f"{L['code']}: SKU-{random.randint(10000,99999)}",
                 f"{L['batch']}: {meta['batch_lot_number']}   {L['origin']}: {meta['country_of_origin']}",
                 f"{L['storage']}: {meta['storage_conditions']}"]:
        c.drawString(18*mm, y, line); y -= 5.5*mm
    y -= 4*mm

    c.setFont("Helvetica-Bold", 10); c.drawString(18*mm, y, L["ingredients"] + ":"); y -= 6*mm
    c.setFont("Helvetica", 9)
    for line in textwrap.wrap(", ".join(ingredients) + ".", width=95):
        c.drawString(18*mm, y, line); y -= 5*mm
    y -= 6*mm

    c.setFont("Helvetica-Bold", 10); c.drawString(18*mm, y, L["matrix_title"]); y -= 7*mm
    c.setFont("Helvetica", 7)
    col_w = 12*mm; x0 = 18*mm
    for i, key in enumerate(ALLERGEN_KEYS):
        cx = x0 + i * col_w
        c.saveState(); c.translate(cx + 3, y - 2); c.rotate(60)
        c.drawString(0, 0, ALLERGENS[key][lang][:16]); c.restoreState()
    y -= 20*mm
    c.setFont("Helvetica", 9)
    for i, key in enumerate(ALLERGEN_KEYS):
        cx = x0 + i * col_w
        c.rect(cx, y, col_w - 1*mm, 6*mm)
        mark = "X" if key in contains_keys else ("T" if key in traces_keys else "-")
        c.drawCentredString(cx + (col_w-1*mm)/2, y + 2*mm, mark)
    y -= 12*mm
    c.setFont("Helvetica-Oblique", 8); c.drawString(18*mm, y, L["matrix_note"])
    c.save()
    return gt_record(fname, lang, "matrix", product, supplier, contains_keys, traces_keys, ingredients, meta, pair_id)

# ---------- Layout 3: PROSE ----------
def layout_prose(idx, lang, contains_keys, traces_keys):
    L = LABELS_TEXT[lang]
    product = random.choice(PRODUCT_NAMES[lang])
    supplier = random.choice(SUPPLIER_NAMES)
    meta = make_meta(lang)
    ingredients = build_ingredient_list(lang, contains_keys)
    pair_id = f"doc_{idx:04d}"
    fname = f"{idx:04d}_prose_{lang}.pdf"
    path = os.path.join(PDF_DIR, fname)

    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=20*mm, bottomMargin=20*mm, leftMargin=20*mm, rightMargin=20*mm)
    styles = getSampleStyleSheet()
    story = [Paragraph(f"<b>{supplier}</b>", styles["Heading1"]),
             Paragraph(f"{L['spec_sheet']} — {product}", styles["Heading3"]),
             Paragraph(f"{meta['supplier_address']}", styles["Normal"]), Spacer(1, 8)]

    intro = {
        "en": f"This product is prepared using the following ingredients: {', '.join(ingredients)}. ",
        "es": f"Este producto se elabora con los siguientes ingredientes: {', '.join(ingredients)}. ",
        "ca": f"Aquest producte s'elabora amb els següents ingredients: {', '.join(ingredients)}. ",
    }[lang]
    body = intro
    if contains_keys:
        names = ", ".join(ALLERGENS[k][lang] for k in contains_keys)
        body += {"en": f"Please note this product contains the following allergens: {names}. ",
                 "es": f"Tenga en cuenta que este producto contiene los siguientes alergenos: {names}. ",
                 "ca": f"Tingueu en compte que aquest producte conté els següents al·lergens: {names}. "}[lang]
    if traces_keys:
        names = ", ".join(ALLERGENS[k][lang] for k in traces_keys)
        body += {"en": f"Due to shared production lines, it may also contain traces of {names}. ",
                 "es": f"Debido a lineas de produccion compartidas, tambien puede contener trazas de {names}. ",
                 "ca": f"A causa de línies de producció compartides, també pot contenir traces de {names}. "}[lang]
    body += {"en": f"{L['storage']}: {meta['storage_conditions']}. {L['batch']}: {meta['batch_lot_number']}.",
             "es": f"{L['storage']}: {meta['storage_conditions']}. {L['batch']}: {meta['batch_lot_number']}.",
             "ca": f"{L['storage']}: {meta['storage_conditions']}. {L['batch']}: {meta['batch_lot_number']}."}[lang]
    story.append(Paragraph(body, styles["Normal"]))
    doc.build(story)
    return gt_record(fname, lang, "prose", product, supplier, contains_keys, traces_keys, ingredients, meta, pair_id)

# ---------- Layout 4: FOOTNOTE TRACES ----------
def layout_footnote_traces(idx, lang, contains_keys, traces_keys):
    L = LABELS_TEXT[lang]
    product = random.choice(PRODUCT_NAMES[lang])
    supplier = random.choice(SUPPLIER_NAMES)
    meta = make_meta(lang)
    ingredients = build_ingredient_list(lang, contains_keys)
    pair_id = f"doc_{idx:04d}"
    fname = f"{idx:04d}_footnote_{lang}.pdf"
    path = os.path.join(PDF_DIR, fname)

    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=20*mm, bottomMargin=15*mm, leftMargin=18*mm, rightMargin=18*mm)
    styles = getSampleStyleSheet()
    tiny = ParagraphStyle("tiny", parent=styles["Normal"], fontSize=6.5, textColor=colors.grey)
    story = [Paragraph(f"<b>{L['spec_sheet']}</b> — {product}", styles["Title"]),
             Paragraph(f"{L['supplier']}: {supplier}  |  {L['batch']}: {meta['batch_lot_number']}", styles["Normal"]),
             Spacer(1, 8),
             Paragraph(f"<b>{L['ingredients']}</b>: " + ", ".join(ingredients) + ".", styles["Normal"]),
             Spacer(1, 6)]
    if contains_keys:
        names = ", ".join(ALLERGENS[k][lang] for k in contains_keys)
        story.append(Paragraph(f"<b>{L['contains']}:</b> {names}.", styles["Normal"]))
    story.append(Spacer(1, 34))
    if traces_keys:
        names = ", ".join(ALLERGENS[k][lang] for k in traces_keys)
        footnote = {"en": f"* Manufactured in a facility that also processes {names}. {L['may_contain']} {names}.",
                    "es": f"* Fabricado en una instalacion que tambien procesa {names}. {L['may_contain']} {names}.",
                    "ca": f"* Fabricat en una instal·lacio que tambe processa {names}. {L['may_contain']} {names}."}[lang]
        story.append(Paragraph(footnote, tiny))
    story.append(Paragraph(f"{L['storage']}: {meta['storage_conditions']}", tiny))
    doc.build(story)
    return gt_record(fname, lang, "footnote_traces", product, supplier, contains_keys, traces_keys, ingredients, meta, pair_id)

# ---------- Layout 5: FREE-FROM negation ----------
def layout_free_from(idx, lang, contains_keys, traces_keys):
    L = LABELS_TEXT[lang]
    product = random.choice(PRODUCT_NAMES[lang])
    supplier = random.choice(SUPPLIER_NAMES)
    meta = make_meta(lang)
    remaining = [k for k in ALLERGEN_KEYS if k not in contains_keys and k not in traces_keys]
    free_from_keys = random.sample(remaining, min(3, len(remaining))) if remaining else []
    ingredients = build_ingredient_list(lang, contains_keys)
    pair_id = f"doc_{idx:04d}"
    fname = f"{idx:04d}_freefrom_{lang}.pdf"
    path = os.path.join(PDF_DIR, fname)

    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=20*mm, bottomMargin=20*mm, leftMargin=18*mm, rightMargin=18*mm)
    styles = getSampleStyleSheet()
    story = [Paragraph(f"<b>{L['spec_sheet']}</b>", styles["Title"]),
             Paragraph(f"{L['product']}: {product}", styles["Normal"]),
             Paragraph(f"{L['supplier']}: {supplier}", styles["Normal"]),
             Paragraph(f"{L['origin']}: {meta['country_of_origin']}   {L['net_weight']}: {meta['net_weight']}", styles["Normal"]),
             Spacer(1, 8),
             Paragraph(f"<b>{L['ingredients']}</b>: " + ", ".join(ingredients) + ".", styles["Normal"]),
             Spacer(1, 6)]
    if contains_keys:
        names = ", ".join(ALLERGENS[k][lang] for k in contains_keys)
        story.append(Paragraph(f"<b>{L['contains']}:</b> {names}.", styles["Normal"]))
    free_names = ", ".join(ALLERGENS[k][lang] for k in free_from_keys)
    story.append(Paragraph(f"<b>{L['free_from']}:</b> {free_names}.", styles["Normal"]))
    doc.build(story)
    rec = gt_record(fname, lang, "free_from", product, supplier, contains_keys, traces_keys, ingredients, meta, pair_id)
    rec["allergens_explicitly_free_from"] = sorted(free_from_keys)
    return rec

# ---------- Layout 6: BILINGUAL (NEW — fixes v1 Minor Problem #11) ----------
def layout_bilingual(idx, lang_main, contains_keys, traces_keys):
    lang_secondary = random.choice([l for l in LANGS if l != lang_main])
    L1, L2 = LABELS_TEXT[lang_main], LABELS_TEXT[lang_secondary]
    product = random.choice(PRODUCT_NAMES[lang_main])
    supplier = random.choice(SUPPLIER_NAMES)
    meta = make_meta(lang_main)
    ingredients = build_ingredient_list(lang_main, contains_keys)
    pair_id = f"doc_{idx:04d}"
    fname = f"{idx:04d}_bilingual_{lang_main}-{lang_secondary}.pdf"
    path = os.path.join(PDF_DIR, fname)

    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=18*mm, bottomMargin=18*mm, leftMargin=18*mm, rightMargin=18*mm)
    styles = getSampleStyleSheet()
    story = [Paragraph(f"<b>{L1['spec_sheet']} / {L2['spec_sheet']}</b>", styles["Title"]),
             Paragraph(f"{product}", styles["Heading2"]),
             Paragraph(f"{L1['supplier']} / {L2['supplier']}: {supplier}", styles["Normal"]),
             Spacer(1, 8),
             Paragraph(f"<b>{L1['ingredients']} / {L2['ingredients']}</b>: " + ", ".join(ingredients) + ".", styles["Normal"]),
             Spacer(1, 8)]
    # Allergen declaration deliberately given ONLY in the secondary language footer —
    # a common real-world pattern (main body in one language, allergen block in another)
    if contains_keys:
        names = ", ".join(ALLERGENS[k][lang_secondary] for k in contains_keys)
        story.append(Paragraph(f"<b>{L2['contains']} ({lang_secondary.upper()}):</b> {names}.", styles["Normal"]))
    if traces_keys:
        names = ", ".join(ALLERGENS[k][lang_secondary] for k in traces_keys)
        story.append(Paragraph(f"<i>{L2['may_contain']} ({lang_secondary.upper()}): {names}.</i>", styles["Normal"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"{L1['batch']}: {meta['batch_lot_number']} | {L1['origin']}: {meta['country_of_origin']}", styles["Normal"]))
    doc.build(story)
    rec = gt_record(fname, lang_main, "bilingual", product, supplier, contains_keys, traces_keys, ingredients, meta, pair_id)
    rec["language_secondary"] = lang_secondary
    rec["allergen_declaration_language"] = lang_secondary  # NOTE: differs from main doc language — important edge case
    return rec

# ------------------------------------------------------------------
LAYOUT_FUNCS = {
    "table": layout_table, "matrix": layout_matrix, "prose": layout_prose,
    "footnote_traces": layout_footnote_traces, "free_from": layout_free_from, "bilingual": layout_bilingual,
}

def main(n_per_layout_per_lang=14):
    records = []
    idx = 1
    for layout_name, layout_fn in LAYOUT_FUNCS.items():
        for lang in LANGS:
            for _ in range(n_per_layout_per_lang):
                contains_keys = pick_allergens(1, 4)
                remaining = [k for k in ALLERGEN_KEYS if k not in contains_keys]
                traces_keys = random.sample(remaining, random.choice([0,0,1,1,2])) if remaining else []
                rec = layout_fn(idx, lang, contains_keys, traces_keys)
                records.append(rec)
                idx += 1
    # negative controls (zero-allergen docs) — proportional to new dataset size
    for lang in LANGS:
        for _ in range(4):
            rec = layout_table(idx, lang, [], [])
            records.append(rec); idx += 1

    with open(os.path.join(OUT_DIR, "ground_truth.jsonl"), "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Generated {len(records)} clean PDFs across {len(LAYOUT_FUNCS)} layouts x {len(LANGS)} languages.")
    print("Allergen 'contains' balance:", dict(SAMPLER.counts))
    return records

if __name__ == "__main__":
    main()
