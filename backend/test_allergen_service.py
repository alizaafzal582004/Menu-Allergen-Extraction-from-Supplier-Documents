from app.mineru_service import run_mineru_extraction
from app.allergen_service import detect_allergens
import json

pdf_path = "uploaded_files/0235_bilingual_es-ca.pdf"

extracted_text = run_mineru_extraction(pdf_path)
print("✅ MinerU extraction done.")

result = detect_allergens(extracted_text)
print("✅ Allergen detection done.")
print(json.dumps(result, indent=2, ensure_ascii=False))