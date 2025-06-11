from dotenv import load_dotenv
import os
from pathlib import Path
from chatbot_theme_identifier.logger import logging
from chatbot_theme_identifier.exception import customexception
import sys

class load_config():
    def __init__(self):
            pass

    def load_config(self):
            # Load environment variables from .env file
            
            try:
                load_dotenv()

                # Retrieve the GROQ API key
                groq_api_key = os.getenv("GROQ_API_KEY")
                if not groq_api_key:
                    raise ValueError("GROQ_API_KEY not found in .env")

                # Set up the upload directory
                upload_dir = Path("/tmp/uploads")
                upload_dir.mkdir(parents=True, exist_ok=True)

                # Return the config values
                return {
                    "GROQ_API_KEY": groq_api_key,
                    "UPLOAD_DIR": upload_dir
                }
    
            except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)

  

