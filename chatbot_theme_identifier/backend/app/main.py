
from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
from typing import List, Optional
from chatbot_theme_identifier.backend.app.config import load_config
from chatbot_theme_identifier.backend.app.service import service
from chatbot_theme_identifier.logger import logging
from chatbot_theme_identifier.exception import customexception
from chatbot_theme_identifier.backend.app.core import core
service=service()
core=core()
config=load_config()
config=config.load_config()
app = FastAPI()
UPLOAD_DIR = config["UPLOAD_DIR"]
os.makedirs(UPLOAD_DIR, exist_ok=True)
# Serve uploaded files at /uploads/<filename>
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
documents_cache = []  # Temporary in-memory storage



@app.get("/", response_class=HTMLResponse)
async def home():
    return core.home()


@app.post("/upload")
async def upload_files(files: List[UploadFile]):
    return core.upload_files(files)


@app.get("/query", response_class=HTMLResponse)
async def query_form():
    return core.query_form()


@app.post("/ask", response_class=HTMLResponse)
async def ask_question(query: str = Form(...),selected_files: Optional[List[str]] = Form(None)):
    return core.ask_question(query,selected_files)



    