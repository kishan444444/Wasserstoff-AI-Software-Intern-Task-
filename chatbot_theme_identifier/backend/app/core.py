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
import sys
service=service()
config=load_config()
config=config.load_config()
app = FastAPI()
UPLOAD_DIR = config["UPLOAD_DIR"]
os.makedirs(UPLOAD_DIR, exist_ok=True)
# Serve uploaded files at /uploads/<filename>
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
documents_cache = []  # Temporary in-memory storage

class core():
    
    def __init__(self):
            pass
            

    def home(self):
        
        try:
            return HTMLResponse(content="""
                <html>
                <head>
                    <title>Upload & Ask</title>
                    <style>
                        body, html {
                            height: 100%;
                            margin: 0;
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            background: linear-gradient(135deg, #e0f7fa, #e1bee7);
                            display: flex;
                            justify-content: center;
                            align-items: center;
                        }
                        .content {
                            text-align: center;
                            color: #333;
                        }
                        h1 {
                            font-size: 3rem;
                            margin-bottom: 30px;
                        }
                        form {
                            display: inline-block;
                        }
                        input[type="file"] {
                            padding: 10px;
                            border-radius: 5px;
                            background-color: #fff;
                            border: 1px solid #ccc;
                            margin-bottom: 20px;
                        }
                        button {
                            display: block;
                            margin: 0 auto;
                            background-color: #6200ea;
                            color: white;
                            border: none;
                            padding: 12px 24px;
                            font-size: 1rem;
                            border-radius: 5px;
                            cursor: pointer;
                            transition: background-color 0.3s ease;
                        }
                        button:hover {
                            background-color: #3700b3;
                        }
                    </style>
                </head>
                <body>
                    <div class="content">
                        <h1>Upload Your Files</h1>
                        <form action="/upload" method="post" enctype="multipart/form-data">
                            <input type="file" name="files" multiple required><br>
                            <button type="submit">Upload</button>
                        </form>
                    </div>
                </body>
                </html>
            """)
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)




    def upload_files(self,files: List[UploadFile]):
            
        try:
            file_paths = []
            for file in files:
                file_path = os.path.join(UPLOAD_DIR, file.filename)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                file_paths.append(file_path)

            global documents_cache
            documents_cache = service.process_paths(file_paths)

            return RedirectResponse(url="/query", status_code=303)
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)
        
    def query_form(self):
            
        try:
            files = [doc['filename'] for doc in documents_cache]
            if not files:
                return HTMLResponse(content="""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>No Documents</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                    <style>
                        body {
                            height: 100vh;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            background: linear-gradient(to right, #83a4d4, #b6fbff);
                            font-family: 'Segoe UI', sans-serif;
                        }
                    </style>
                </head>
                <body>
                    <div class="text-center bg-white p-5 rounded shadow" style="max-width: 500px;">
                        <h2 class="mb-3">No Documents Uploaded Yet</h2>
                        <a href="/" class="btn btn-primary btn-lg">Upload Files</a>
                    </div>
                </body>
                </html>
                """)

            return HTMLResponse(content=f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>Query Documents</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        font-family: 'Segoe UI', sans-serif;
                        background: linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%);
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }}
                    .card {{
                        background: white;
                        padding: 40px;
                        border-radius: 20px;
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                        width: 100%;
                        max-width: 800px;
                    }}
                    h1 {{
                        font-size: 2.5rem;
                        margin-bottom: 30px;
                        text-align: center;
                    }}
                    .form-check {{
                        margin-bottom: 10px;
                    }}
                    .uploaded-file {{
                        margin-bottom: 10px;
                    }}
                    .uploaded-img {{
                        max-width: 100px;
                        max-height: 100px;
                        border-radius: 8px;
                        margin-top: 5px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }}
                    .btn-primary {{
                        background-color: #6f42c1;
                        border: none;
                    }}
                    .btn-primary:hover {{
                        background-color: #5936a7;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>Ask Questions About Your Documents</h1>
                    <div class="mb-4">
                        <h5>Uploaded Files</h5>
                        <ul class="list-group mb-3">
                            {"".join(
                                f'''
                                <li class="list-group-item uploaded-file">
                                    <a href="/uploads/{f}" target="_blank">{f}</a>
                                    {'<br><img src="/uploads/' + f + '" class="uploaded-img">' if f.lower().endswith(('.png', '.jpg', '.jpeg')) else ''}
                                </li>
                                '''
                                for f in files
                            )}
                        </ul>
                    </div>
                    <form method="post" action="/ask">
                        <div class="mb-4">
                            <h5>Select Documents to Query:</h5>
                            {"".join(
                                f'''
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" name="selected_files" value="{f}" id="{f}" checked>
                                    <label class="form-check-label" for="{f}">{f}</label>
                                </div>
                                '''
                                for f in files
                            )}
                        </div>
                        <div class="mb-4">
                            <label for="query" class="form-label">Enter Your Question</label>
                            <input type="text" class="form-control form-control-lg" id="query" name="query" placeholder="Ask something smart..." required>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">Ask</button>
                        </div>
                    </form>
                    <div class="text-center mt-4">
                        <a href="/" class="btn btn-link">⬅ Upload More Files</a>
                    </div>
                </div>
            </body>
            </html>
            """)
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)
            
    def query_form(self):
            
        try:
            files = [doc['filename'] for doc in documents_cache]
            if not files:
                return HTMLResponse(content="""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>No Documents</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                    <style>
                        body {
                            height: 100vh;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            background: linear-gradient(to right, #83a4d4, #b6fbff);
                            font-family: 'Segoe UI', sans-serif;
                        }
                    </style>
                </head>
                <body>
                    <div class="text-center bg-white p-5 rounded shadow" style="max-width: 500px;">
                        <h2 class="mb-3">No Documents Uploaded Yet</h2>
                        <a href="/" class="btn btn-primary btn-lg">Upload Files</a>
                    </div>
                </body>
                </html>
                """)

            return HTMLResponse(content=f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>Query Documents</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        font-family: 'Segoe UI', sans-serif;
                        background: linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%);
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }}
                    .card {{
                        background: white;
                        padding: 40px;
                        border-radius: 20px;
                        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                        width: 100%;
                        max-width: 800px;
                    }}
                    h1 {{
                        font-size: 2.5rem;
                        margin-bottom: 30px;
                        text-align: center;
                    }}
                    .form-check {{
                        margin-bottom: 10px;
                    }}
                    .uploaded-file {{
                        margin-bottom: 10px;
                    }}
                    .uploaded-img {{
                        max-width: 100px;
                        max-height: 100px;
                        border-radius: 8px;
                        margin-top: 5px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }}
                    .btn-primary {{
                        background-color: #6f42c1;
                        border: none;
                    }}
                    .btn-primary:hover {{
                        background-color: #5936a7;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>Ask Questions About Your Documents</h1>
                    <div class="mb-4">
                        <h5>Uploaded Files</h5>
                        <ul class="list-group mb-3">
                            {"".join(
                                f'''
                                <li class="list-group-item uploaded-file">
                                    <a href="/uploads/{f}" target="_blank">{f}</a>
                                    {'<br><img src="/uploads/' + f + '" class="uploaded-img">' if f.lower().endswith(('.png', '.jpg', '.jpeg')) else ''}
                                </li>
                                '''
                                for f in files
                            )}
                        </ul>
                    </div>
                    <form method="post" action="/ask">
                        <div class="mb-4">
                            <h5>Select Documents to Query:</h5>
                            {"".join(
                                f'''
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" name="selected_files" value="{f}" id="{f}" checked>
                                    <label class="form-check-label" for="{f}">{f}</label>
                                </div>
                                '''
                                for f in files
                            )}
                        </div>
                        <div class="mb-4">
                            <label for="query" class="form-label">Enter Your Question</label>
                            <input type="text" class="form-control form-control-lg" id="query" name="query" placeholder="Ask something smart..." required>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">Ask</button>
                        </div>
                    </form>
                    <div class="text-center mt-4">
                        <a href="/" class="btn btn-link">⬅ Upload More Files</a>
                    </div>
                </div>
            </body>
            </html>
            """)
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)




    def ask_question(self,query: str = Form(...),selected_files: Optional[List[str]] = Form(None)):
            
        try:
            selected = selected_files if selected_files else [doc['filename'] for doc in documents_cache]

            answers = service.query_documents(documents_cache, query, selected_filenames=selected)
            summary = service.synthesize_themes(answers)

            
            answer_html = """
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <div class="container mt-5">
                <h2 class="mb-4">Individual Document Responses</h2>
                <table class="table table-bordered table-striped align-middle">
                    <thead class="table-light">
                        <tr>
                            <th>Document ID</th>
                            <th>Extracted Answer</th>
                            <th>Citation</th>
                        </tr>
                    </thead>
                    <tbody>
                    """

            for idx, a in enumerate(answers, start=1):
                page, paragraph, cleaned_answer = service.extract_first_citation_info(a["answer"])
                doc_id = f"DOC{idx:03}"  # e.g., DOC001, DOC002
                citation = f"Page {page}, Para {paragraph}" if page and paragraph else "—"

                answer_html += f"""
                    <tr>
                        <td>{doc_id}</td>
                        <td>{cleaned_answer}</td>
                        <td>{citation}</td>
                    </tr>
                """

            answer_html += """
                        </tbody>
                    </table>
                </div>
            """



                

            return HTMLResponse(content=f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <title>Results</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                </head>
                <body class="container mt-4">
                <h1>Query: {query}</h1>
                <h2>Answers:</h2>
                <ul>{answer_html}</ul>
                <h2>Synthesized Summary:</h2>
                <p>{summary}</p>
                <a href="/query" class="btn btn-secondary mt-3">Back to Query</a>
                <a href="/" class="btn btn-link mt-3">Upload More Files</a>
                </body>
                </html>
            """)
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)
    
    



        
        
    
        