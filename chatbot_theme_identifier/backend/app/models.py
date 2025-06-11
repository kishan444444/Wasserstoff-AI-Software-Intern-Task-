from langchain_groq import ChatGroq
from langchain.embeddings import SentenceTransformerEmbeddings
from chatbot_theme_identifier.backend.app.config import load_config
from chatbot_theme_identifier.logger import logging
from chatbot_theme_identifier.exception import customexception
import sys

config = load_config()
config = config.load_config()

class InitializeModels:
    def __init__(self):
        pass

    def initialize_models(self):
        try:
            GROQ_API_KEY = config["GROQ_API_KEY"]

            # Initialize the ChatGroq model
            model = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)

            # Initialize the sentence transformer for embeddings
            embeddings_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

            return model, embeddings_model

        except Exception as e:
            logging.info("Exception occurred in load_object file utils")
            raise customexception(e, sys)

        
