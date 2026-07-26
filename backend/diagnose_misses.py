from app.mineru_service import run_mineru_extraction

pdfs_to_check = [
    "0043_matrix_en.pdf",
    "0128_footnote_en.pdf",
    "0170_freefrom_en.pdf",
]

DATASET_PDFS_DIR = r"C:\barcelona-bites-allergen-ai\ml\data\barcelona_bites_synthetic_dataset_v2\barcelona_bites_synthetic_dataset_v2\pdfs"

import os

for pdf_filename in pdfs_to_check:
    pdf_path = os.path.join(DATASET_PDFS_DIR, pdf_filename)
    print(f"\n{'='*60}")
    print(f"FILE: {pdf_filename}")
    print(f"{'='*60}")
    extracted_text = run_mineru_extraction(pdf_path)
    print(extracted_text)