from fastapi import FastAPI

app = FastAPI(title="Barcelona Bites - Allergen Extraction API")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "allergen-extraction-api"}