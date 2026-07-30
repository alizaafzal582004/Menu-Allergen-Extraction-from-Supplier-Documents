# 🍽️ Menu & Allergen Extraction from Supplier Documents

<div align="center">

### **Stop manually reading supplier PDFs. Let AI do it in seconds.**

**An AI-powered Document Intelligence system that automatically extracts menu items, ingredients, and allergens from supplier specification documents.**

---

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge\&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?style=for-the-badge\&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=for-the-badge\&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge\&logo=postgresql)
![AI](https://img.shields.io/badge/AI-Document%20Intelligence-purple?style=for-the-badge)
![OCR](https://img.shields.io/badge/OCR-Automated-orange?style=for-the-badge)

**Built for real-world restaurant operations where missing a single allergen can put customer safety at risk.**

</div>

---

#  Why This Project?

Every day, restaurants receive supplier specification sheets in PDF format.

Staff members spend hours manually reading documents and copying:

* Ingredients
* Allergens
* Product names
* Menu information

Manual work is:

* ❌ Slow
* ❌ Expensive
* ❌ Error-prone
* ❌ Dangerous if allergens are missed

This project automates the entire process using AI.

Upload a supplier PDF and receive structured ingredient and allergen information within seconds.

---

#  Business Problem

Restaurants often manage hundreds of supplier documents.

Each document may contain:

* Product descriptions
* Ingredient lists
* Nutrition information
* Allergen declarations

Manually extracting this information increases the risk of:

* Incorrect menu data
* Human error
* Regulatory issues
* Customer health risks
* Operational delays

This system eliminates repetitive manual work while improving accuracy and consistency.

---

#  Solution

This application uses AI-powered document understanding to:

* 📄 Read supplier PDFs
* 🔍 Extract structured text
* 🥗 Detect ingredients
* ⚠️ Identify allergens
* 💾 Store results in a database
* 🌐 Expose everything through REST APIs

---

#  Features

* Upload Supplier PDF
* OCR & Document Parsing
* Automatic Ingredient Extraction
* Automatic Allergen Detection
* Structured JSON Output
* Confidence Scores
* Human Review Support
* FastAPI Backend
* PostgreSQL Database
* Docker Ready
* REST API
* Logging
* Scalable Architecture

---

#  Project Architecture

```text
Supplier PDF
      │
      ▼
 Document Processing
      │
      ▼
 OCR & Layout Analysis
      │
      ▼
 AI Extraction Engine
      │
      ├────────► Ingredients
      │
      ├────────► Allergens
      │
      └────────► Product Details
                    │
                    ▼
             PostgreSQL Database
                    │
                    ▼
               FastAPI Backend
                    │
                    ▼
              Frontend / Client
```

---

# 🛠️ Tech Stack

| Category         | Technology            |
| ---------------- | --------------------- |
| Language         | Python                |
| Backend          | FastAPI               |
| Database         | PostgreSQL            |
| AI               | Document Intelligence |
| OCR              | MinerU                |
| Containerization | Docker                |
| ORM              | SQLAlchemy            |
| API Testing      | Swagger UI            |
| Version Control  | Git & GitHub          |

---

#  Project Structure

```bash
Menu-Allergen-Extraction/
│
├── app/
│   ├── models/
│   ├── services/
│   ├── routes/
│   ├── database/
│   ├── utils/
│   └── main.py
│
├── uploads/
├── outputs/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# ⚙️ Workflow

```text
Upload PDF
      ↓
Extract Text
      ↓
Understand Document
      ↓
Extract Ingredients
      ↓
Detect Allergens
      ↓
Store Results
      ↓
Return JSON Response
```

---

# 📊 Example Output

```json
{
  "product": "Chicken Burger",
  "ingredients": [
    "Chicken",
    "Wheat Flour",
    "Milk Powder",
    "Soy Protein"
  ],
  "allergens": [
    "Gluten",
    "Milk",
    "Soy"
  ],
  "confidence": 0.97
}
```

---
<img width="1108" height="717" alt="image" src="https://github.com/user-attachments/assets/edb71a72-80fc-419d-92db-d3a593cf42f8" />
<img width="1162" height="860" alt="image" src="https://github.com/user-attachments/assets/c28cc099-b402-4571-a547-14b5a3f5f921" />

---
# 🎯 Real-World Applications

* Restaurants
* Food Chains
* Hotels
* Cloud Kitchens
* Food Manufacturers
* Catering Companies
* Food Safety Compliance
* Menu Management Systems

---

# 🔥 Why This Project Matters

Food allergies are a serious health concern.

Missing just one allergen can lead to:

* Severe allergic reactions
* Customer safety incidents
* Legal consequences
* Financial losses
* Brand reputation damage

This project helps businesses reduce these risks through AI-powered automation.

---

# 🚧 Future Improvements

* Multi-language document support
* Image-based specification sheets
* Nutrition extraction
* Barcode integration
* AI confidence visualization
* Human-in-the-loop validation
* Supplier comparison
* Batch document processing
* Dashboard & Analytics
* Cloud deployment

---

# 📈 Project Goals

* Reduce manual data entry
* Improve extraction accuracy
* Minimize allergen-related risks
* Speed up restaurant operations
* Build a production-ready AI pipeline

---

# 🤝 Contributing

Contributions, ideas, feature requests, and pull requests are always welcome.

If you'd like to improve this project, feel free to fork the repository and submit a PR.

---

# ⭐ If You Found This Useful

Please consider giving this repository a **Star ⭐**

It helps others discover the project and motivates further development.

---

<div align="center">

### **Building AI that makes restaurants safer, smarter, and more efficient.**

**Made with ❤️ using Python, FastAPI, AI & Document Intelligence**

</div>
