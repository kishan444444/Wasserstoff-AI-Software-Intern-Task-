# AI Software Intern – Internship Task

# AI-Powered Document Research Chatbot

## Project Overview

This project aims to develop a robust web-based chatbot capable of ingesting, processing, and querying a large collection of documents (including scanned PDFs and images). It leverages OCR and modern AI language models to enable deep research capabilities with theme identification and precise citations.

---
## Task Breakdown

### 1. Document Upload and Knowledge Base Creation
- Support uploading 75+ documents in various formats including PDFs and scanned images.
- Convert and preprocess scanned documents using Optical Character Recognition (OCR).
- Extract text content with high accuracy, ensuring fidelity for research.
- Store and integrate uploaded documents in a database for efficient reuse.

### 2. Document Management & Query Processing
- Provide an intuitive interface to view all uploaded documents.
- Allow users to submit natural language queries.
- Process each query against individual documents.
- Extract relevant answers with precise citations indicating page, paragraph, and sentence locations.

### 3. Theme Identification & Cross-Document Synthesis
- Analyze responses across all documents collectively.
- Identify coherent common themes across multiple documents (multiple themes supported).
- Generate a final synthesized answer with clear indication of all themes.
- Map citations comprehensively at least to the document level to support each synthesized theme.

### Additional Functionalities (Extra Credit)
- Provide citation granularity down to paragraph or sentence level.
- Visual representation or citation-document mapping interface.
- Advanced filtering options (e.g., date, author, document type, relevance).
- Enable selection or deselection of specific documents for targeted querying.

---

## Technical Requirements

- **AI Language Models:** OpenAI GPT, Gemini, Groq (free credits available for GPT and Gemini; Groq hosts LLAMA).
- **Vector Databases:** Qdrant, ChromaDB, FAISS for efficient semantic search.
- **OCR Tools:** Tesseract, PaddleOCR for scanned document text extraction.
- **Backend Frameworks:** Python FastAPI or Flask.
- **Deployment:** Preferably on free hosting platforms (see deployment instructions).

---

## Deliverables

- Fully functional web-based chatbot with clean, documented code.
- Brief technical report outlining methodologies and technologies.
- Demonstration video or presentation showcasing features and performance.

---

## Features

- **Functionality:** Completeness in document research, theme extraction, and citation accuracy.
- **Code Quality & Structure:** Modular design, clear naming conventions, comments, and version control usage.
- **Error Handling:** Robust handling of edge cases and failures.
- **Documentation:** Clear, comprehensive README and demonstration material.
- **System Design Insight:** Considerations for scalability and deployment.
- **User Interface:** Simplicity and clarity for end-users.

---


## Repository Structure


```
chatbot_theme_identifier/ 
├── backend/ 
│   ├── app/ 
│   │   ├── api/ 
│   │   ├── core/ 
│   │   ├── models/ 
│   │   ├── services/ 
│   │   ├── main.py 
│   │   └── config.py 
│   ├── data/ 
│   ├── Dockerfile 
│   └── requirements.txt 
├── docs/ 
├── tests/ 
├── demo/ 
└── README.md
```



## Getting Started

### Prerequisites

* Python 3.10 or higher
* Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kishan444444/AI-Software-Intern---Internship-Task.git
   cd AI-Software-Intern---Internship-Task
   ```

2. **Run the application:**

   ```bash
   uvicorn backend.app.main:app --reload
   ```

### Using Docker

1. **Build the Docker image:**

   ```bash
   docker build -t ai-chatbot .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -it ai-chatbot
   ```

## Usage

Upon running the application, the chatbot will prompt for user input. Enter your messages, and the chatbot will respond based on the identified theme.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or feedback, please contact [kishanverma4444@gmail.com].





