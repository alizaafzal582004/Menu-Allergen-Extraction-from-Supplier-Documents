FROM python:3.11-slim

WORKDIR /app

# System dependencies MinerU aur PDF-processing ke liye zaroori
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies pehle copy aur install karo (Docker caching optimize karne ke liye)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki app code copy karo
COPY . .

# Uploaded files aur MinerU output ke liye folders banao
RUN mkdir -p uploaded_files mineru_output

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]