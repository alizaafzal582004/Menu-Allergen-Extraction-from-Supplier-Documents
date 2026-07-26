from app.mineru_service import run_mineru_extraction

pdf_path = "uploaded_files/0235_bilingual_es-ca.pdf"

extracted_text = run_mineru_extraction(pdf_path)

print("✅ Extraction successful!")
print(extracted_text)