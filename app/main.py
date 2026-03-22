from fastapi import FastAPI
from app.api.routes import api_router
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(
    title="LinguaMate Backend",
    description="AI-powered language learning backend",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "LinguaMate backend is running 🚀"}

app.include_router(api_router)

# For local running
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000)) # Render compatible
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)