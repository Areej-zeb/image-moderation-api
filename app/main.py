from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.routes import api_router
from app.core.config import MONGO_URI

app = FastAPI(title="Image Moderation API")

# Connect routes
app.include_router(api_router)

# Print MongoDB connection URI (debug)
print(f"🔗 CONNECTING TO MONGO URI: {MONGO_URI}")

# CORS middleware for browser and Postman
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve index.html at "/"
@app.get("/")
def serve_frontend():
    index_path = os.path.join("app", "static", "index.html")
    return FileResponse(index_path)
