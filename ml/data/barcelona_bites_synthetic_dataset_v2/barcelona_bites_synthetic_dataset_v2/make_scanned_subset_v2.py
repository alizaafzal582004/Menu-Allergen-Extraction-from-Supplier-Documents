import os, json, random
from pdf2image import convert_from_path
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

random.seed(99)
OUT_DIR = "/home/claude/synth_dataset_v2"
PDF_DIR = os.path.join(OUT_DIR, "pdfs")
SCAN_DIR = os.path.join(OUT_DIR, "pdfs_scanned")
os.makedirs(SCAN_DIR, exist_ok=True)

TIERS = {
    "mild":     dict(angle=(-2.5, 2.5),  blur=(0.3, 0.8), noise=(5, 12), upside_down_p=0.0),
    "moderate": dict(angle=(-6, 6),      blur=(0.6, 1.4), noise=(10, 20), upside_down_p=0.0),
    "severe":   dict(angle=(-15, 15),    blur=(1.0, 2.2), noise=(18, 32), upside_down_p=0.12),
}

def degrade(img, tier_cfg):
    img = img.convert("L")
    if random.random() < tier_cfg["upside_down_p"]:
        img = img.rotate(180, expand=True, fillcolor=255)
    angle = random.uniform(*tier_cfg["angle"])
    img = img.rotate(angle, expand=True, fillcolor=255)
    img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(*tier_cfg["blur"])))
    arr = np.array(img).astype(np.int16)
    noise = np.random.normal(0, random.uniform(*tier_cfg["noise"]), arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)
    img = ImageEnhance.Contrast(img).enhance(random.uniform(0.8, 1.08))
    img = ImageEnhance.Brightness(img).enhance(random.uniform(0.9, 1.06))
    return img.convert("RGB")

def main(fraction=0.30):
    gt = [json.loads(l) for l in open(os.path.join(OUT_DIR, "ground_truth.jsonl"))]
    n = max(1, int(len(gt) * fraction))
    chosen = random.sample(gt, n)
    # split chosen evenly across the 3 severity tiers
    tier_names = list(TIERS.keys())
    scanned_records = []
    for i, rec in enumerate(chosen):
        tier = tier_names[i % len(tier_names)]
        src = os.path.join(PDF_DIR, rec["file"])
        pages = convert_from_path(src, dpi=150)
        degraded_pages = [degrade(p, TIERS[tier]) for p in pages]
        out_name = rec["file"].replace(".pdf", f"_SCANNED_{tier}.pdf")
        out_path = os.path.join(SCAN_DIR, out_name)
        degraded_pages[0].save(out_path, save_all=True,
                                append_images=degraded_pages[1:] if len(degraded_pages) > 1 else [])
        new_rec = rec.copy()
        new_rec["file"] = out_name
        new_rec["is_scanned_degraded"] = True
        new_rec["scan_severity_tier"] = tier
        new_rec["source_clean_file"] = rec["file"]
        # pair_id stays IDENTICAL to source's pair_id -> used for split-safe grouping
        scanned_records.append(new_rec)
        print(f"[{tier:8s}] {out_name}")

    with open(os.path.join(OUT_DIR, "ground_truth_scanned.jsonl"), "w") as f:
        for r in scanned_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nCreated {len(scanned_records)} scanned/degraded variants across {len(TIERS)} severity tiers.")

if __name__ == "__main__":
    main()
