import nltk
from nltk.tokenize import sent_tokenize
import cv2
import pytesseract
import pdfplumber
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain.prompts import ChatPromptTemplate
from collections import defaultdict
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import os
from typing import List
from langchain_core.prompts import PromptTemplate
from chatbot_theme_identifier.backend.app.models import InitializeModels
import re
from chatbot_theme_identifier.logger import logging
from chatbot_theme_identifier.exception import customexception
import sys


nltk_data_dir = "/tmp/nltk_data"
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)

nltk.download("punkt", download_dir=nltk_data_dir)
nltk.download("stopwords", download_dir=nltk_data_dir)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['document_storage']
collection = db['documents']

initializer = InitializeModels()
model, embeddings_model = initializer.initialize_models()


# Tesseract path (adjust to your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

supported_ext = ['pdf', 'jpg', 'jpeg', 'png', 'tiff']

        
class service():
    
    
    def __init__(self):
            pass       
        
    def preprocess_image(self,image_path):
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")
            # Optional: denoise, blur, or enhance contrast here
            _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return thresh
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)

    def ocr_image(self,image_path):
        try:
            preprocessed = self.preprocess_image(image_path)
            custom_config = r'--oem 3 --psm 6'  # OCR Engine and page segmentation mode
            return pytesseract.image_to_string(preprocessed, config=custom_config)
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)

    def extract_text_from_pdf(self,pdf_path):
        try:
            page_data = []
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    # Extract text by page
                    page_text = page.extract_text() or ""
                    # Optionally split page_text into paragraphs
                    paragraphs = [p.strip() for p in page_text.split('\n\n') if p.strip()]
                    page_data.append({
                        "page": i + 1,
                        "paragraphs": paragraphs
                    })
            return page_data
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)

    def store_document(self,filename, ext, page_data):
        try:
            # Combine full text for search convenience
            full_text = "\n\n".join(
                "\n".join(page["paragraphs"]) for page in page_data
            )
            doc = {
                "filename": filename,
                "format": ext,
                "content": full_text,
                "pages": page_data
            }
            collection.insert_one(doc)
            print(f"[✓] Stored: {filename}")
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)

    def process_file(self,file_path):
        try:
            filename = os.path.basename(file_path)
            ext = filename.lower().split('.')[-1]
            if ext not in supported_ext:
                print(f"[!] Unsupported file skipped: {filename}")
                return None

            if ext == 'pdf':
                page_data = self.extract_text_from_pdf(file_path)
            else:
                # OCR: convert whole image to single paragraph
                text = self.ocr_image(file_path)
                page_data = [{"page": 1, "paragraphs": [text]}]

            self.store_document(filename, ext, page_data)
            return {"filename": filename, "pages": page_data}
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)

    def process_paths(self,paths):
        try:
            documents = []
            for path in paths:
                if os.path.isfile(path):
                    result = self.process_file(path)
                    if result:
                        documents.append(result)
                elif os.path.isdir(path):
                    for root, _, files in os.walk(path):
                        for file in files:
                            result = self.process_file(os.path.join(root, file))
                            if result:
                                documents.append(result)
                else:
                    print(f"[!] Invalid path: {path}")
            return documents
        
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)

        # Split paragraphs into chunks and keep citation info for each chunk

    def chunk_document_pages(self,document):
        try:
            chunks = []
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

            for page_info in document["pages"]:
                page_num = page_info["page"]
                for para_idx, paragraph in enumerate(page_info["paragraphs"]):
                    para_chunks = splitter.split_text(paragraph)
                    for chunk in para_chunks:
                        chunks.append({
                            "text": chunk,
                            "metadata": {
                                "filename": document["filename"],
                                "page": page_num,
                                "paragraph": para_idx + 1
                            }
                        })
            return chunks
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)


        # Query each document individually with citation support
    def query_documents(self,documents, query,selected_filenames=None):
        try:
            filtered_docs = documents
            if selected_filenames:
                filtered_docs = [doc for doc in documents if doc["filename"] in selected_filenames]
            
            
            answers = []

            # Contextualize question prompt for follow-up handling
            contextualize_q_system_prompt = (
                "Given chat history and user question, reformulate to standalone question."
            )
            contextualize_q_prompt = ChatPromptTemplate.from_messages([
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ])

            for doc in  filtered_docs:
                chunks = self.chunk_document_pages(doc)
                if not chunks:
                    continue

                texts = [chunk["text"] for chunk in chunks]
                metadatas = [chunk["metadata"] for chunk in chunks]

                
                embeddings=embeddings_model
                # Create vector store per document
                vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
                retriever = vector_store.as_retriever()
                

                history_aware_retriever = create_history_aware_retriever(
                    llm=model,
                    retriever=retriever,
                    prompt=contextualize_q_prompt
                )

                system_prompt = (
                    "You are an AI assistant. Use the provided context to answer user question.\n"
                    "Include citations with filename, pagenumber, and paragraph.\n\n"
                    "Context:\n{context}\n\nChat History:\n{chat_history}\n\nUser Question:\n{input}"
                )
                qa_prompt = ChatPromptTemplate.from_template(system_prompt)
                question_answer_chain = create_stuff_documents_chain(model, qa_prompt)
                rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

                chat_history = []
                response = rag_chain.invoke({"input": query, "chat_history": chat_history})
                answer = response.get('answer', '')

                # Append answer with citation to list
                answers.append({
                    "filename": doc["filename"],
                    "answer": answer
                })

            return answers
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)




    def extract_first_citation_info(self,answer_text: str):
        try:
            """
            Extracts the first (page, paragraph) citation from the answer string.
            Returns (page, paragraph, cleaned_answer).
            """
            # Looks for: filename: ..., pagenumber: ..., paragraph: ...
            match = re.search(r'filename:\s*([^,]*),\s*pagenumber:\s*(\d+),\s*paragraph:\s*(\d+)', answer_text, re.IGNORECASE)
            if match:
                page = match.group(2)
                paragraph = match.group(3)
                # Optional: remove all such citation mentions from the answer
                cleaned_answer = re.sub(r'filename:\s*[^,]*,\s*pagenumber:\s*\d+,\s*paragraph:\s*\d+', '', answer_text)
                return page, paragraph, cleaned_answer.strip()
            return "-", "-", answer_text
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)


        # Simple theme identification by clustering answers (placeholder)

    def synthesize_themes(self,answers: List[Dict[str, str]], n_themes: int = 3) -> str:
        try:
            texts = [a['answer'] for a in answers]
            filenames = [a['filename'] for a in answers]

            if not texts:
                return "<p>No answers to synthesize.</p>"

            # TF-IDF vectorization
            vectorizer = TfidfVectorizer(stop_words='english')
            X = vectorizer.fit_transform(texts)

            # Clustering
            kmeans = KMeans(n_clusters=min(n_themes, len(answers)), random_state=42)
            labels = kmeans.fit_predict(X)

            # Group answers by cluster
            clustered = defaultdict(list)
            for idx, label in enumerate(labels):
                clustered[label].append((filenames[idx], texts[idx]))

            # Build HTML table
            html = """
            <table class="table table-bordered">
                <thead class="table-light">
                    <tr>
                        <th>Theme</th>
                        <th>Supporting Document</th>
                        <th>Extracted Insight</th>
                    </tr>
                </thead>
                <tbody>
            """

            theme_summary_prompt = PromptTemplate.from_template(
            "Summarize the following insights into a single theme:\n\n{insights}"
        )

            for theme_id, items in clustered.items():
                insights = "\n\n".join(answer for _, answer in items)
                
                # Optional: Use your LLM to synthesize theme insight
                raw_response = model.invoke(theme_summary_prompt.format(insights=insights))
                synthesized = raw_response.content.strip().replace("\n\n", " ").replace("\n", " ")

                
                for fname, _ in items:
                    html += f"""
                    <tr>
                        <td>Theme {theme_id + 1}</td>
                        <td>{fname}</td>
                        <td>{synthesized}</td>
                    </tr>
                    """

            html += "</tbody></table>"
            return html
        except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)
        
    


