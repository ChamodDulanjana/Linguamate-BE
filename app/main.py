from fastapi import FastAPI
from app.api.routes import api_router

app = FastAPI(
    title="LinguaMate Backend",
    description="AI-powered language learning backend",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "LinguaMate backend is running 🚀"}

app.include_router(api_router)
