import os
import shutil
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Document, Ingredient, Allergen
from app.mineru_service import run_mineru_extraction
from app.allergen_service import detect_allergens

app = FastAPI(title="Barcelona Bites - Allergen Extraction API")

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "allergen-extraction-api"}


@app.post("/documents/upload")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_document = Document(filename=file.filename, status="uploaded")
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "id": new_document.id,
        "filename": new_document.filename,
        "status": new_document.status,
        "uploaded_at": new_document.uploaded_at,
    }


@app.post("/documents/{document_id}/process")
def process_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    pdf_path = os.path.join(UPLOAD_DIR, document.filename)

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Uploaded file not found on disk.")

    try:
        document.status = "processing"
        db.commit()

        extracted_text = run_mineru_extraction(pdf_path)
        result = detect_allergens(extracted_text)

        for ingredient_name in result.get("ingredients", []):
            new_ingredient = Ingredient(name=ingredient_name, document_id=document.id)
            db.add(new_ingredient)
            db.flush()  # assigns new_ingredient.id without fully committing yet

            for allergen_entry in result.get("allergens_detected", []):
                if allergen_entry["source_ingredient"] == ingredient_name:
                    allergen_name = allergen_entry["allergen"]

                    allergen = db.query(Allergen).filter(Allergen.name == allergen_name).first()
                    if allergen is None:
                        allergen = Allergen(name=allergen_name)
                        db.add(allergen)
                        db.flush()

                    new_ingredient.allergens.append(allergen)

        document.status = "processed"
        db.commit()

    except Exception as e:
        document.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    db.refresh(document)

    return {
        "document_id": document.id,
        "filename": document.filename,
        "status": document.status,
        "ingredients_found": len(result.get("ingredients", [])),
        "allergens_found": len(result.get("allergens_detected", [])),
    }


@app.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()

    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "status": doc.status,
            "uploaded_at": doc.uploaded_at,
        }
        for doc in documents
    ]


@app.get("/documents/{document_id}")
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    ingredients_data = []
    for ingredient in document.ingredients:
        ingredients_data.append({
            "id": ingredient.id,
            "name": ingredient.name,
            "allergens": [allergen.name for allergen in ingredient.allergens],
        })

    return {
        "id": document.id,
        "filename": document.filename,
        "status": document.status,
        "uploaded_at": document.uploaded_at,
        "ingredients": ingredients_data,
    }