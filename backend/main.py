from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from database import engine, Base
from routes import users, projects, tasks

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Team Task Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")