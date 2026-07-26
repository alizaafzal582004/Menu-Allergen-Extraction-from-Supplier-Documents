import os
import shutil
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Document

app = FastAPI(title="Barcelona Bites - Allergen Extraction API")

UPLOAD_DIR = "uploaded_files"


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