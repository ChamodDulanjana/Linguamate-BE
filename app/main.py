from fastapi import FastAPI

app = FastAPI(
    title="LinguaMate Backend",
    description="AI-powered language learning backend",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "LinguaMate backend is running 🚀"
    }
