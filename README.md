# Linguamate Backend (Linguamate BE)

Linguamate Backend is the server-side application for the **Linguamate AI Language Learning Platform**. It provides APIs for language detection, AI-powered language processing, and supports the mobile and web clients.

This backend is built using **Python** and is designed with scalability and production-readiness in mind.

---

## 🚀 Tech Stack

* **Python 3.10+**
* **FastAPI** (API framework)
* **Uvicorn** (ASGI server)
* **Machine Learning / NLP**
* **fastText Language Identification Model**
* **Docker** (optional, for deployment)

---

## 📂 Project Structure

```
linguamate-be/
│
├── app/
│   ├── main.py            # Application entry point
│   ├── api/               # API routes
│   ├── core/              # Core configs & utilities
│   ├── services/          # Business logic
│   ├── models/            # ML models (NOT committed)
│   └── schemas/           # Request / response schemas
│
├── requirements.txt       # Python dependencies
├── .gitignore
├── README.md
└── docker-compose.yml     # Optional
```

---

## ⚠️ Important: ML Model Setup (Required)

This project uses the **fastText Language Identification model**.

Due to GitHub file size limits, the model file is **NOT included in the repository**.

### 📥 Download the Model

Download the model from the official fastText source:

```
https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
```

### 📁 Place the Model Here

After downloading, place the file in the following path:

```
app/models/lid.176.bin
```

⚠️ Do **NOT** rename the file.

---

## 🧪 Virtual Environment Setup

### Create virtual environment

```bash
python -m venv venv
```

### Activate

**Windows (PowerShell):**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
uvicorn app.main:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

### API Docs

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

---

## 🔐 Environment Variables

Create a `.env` file in the root directory if required:

```env
APP_ENV=development
APP_PORT=8000
```

⚠️ `.env` files are ignored by Git.

---

## 🧹 Git Ignore Rules

The following files are intentionally ignored:

* `__pycache__/`
* `*.pyc`
* `venv/`
* `app/models/*.bin`
* `.env`

These files are either auto-generated or environment-specific.

---

## 🧠 Notes for Developers

* ML models should be downloaded manually or via startup scripts
* Do NOT commit large binary files to GitHub
* Use Docker for consistent deployment environments

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`feature/your-feature-name`)
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 📜 License

This project is for educational and development purposes.

---

## 👤 Author

**Chamod Dulanjana**
Full‑Stack Developer | AI & NLP Enthusiast

---

🔥 Linguamate Backend – powering intelligent language learning
