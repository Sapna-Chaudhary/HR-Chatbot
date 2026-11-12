# HR Chatbot – AI-Powered HR Assistant

## Project Overview
The HR Chatbot is an AI-powered conversational application designed to help employees access HR-related information through natural language queries.

It combines document-based question answering with structured employee data retrieval to provide information about HR policies, attendance, timesheets, and leave balances.

## Key Features
- **HR Policy Q&A:** Answers employee questions using information from the Employee Handbook.
- **Employee Information Retrieval:** Retrieves employee-related information from Excel datasets.
- **Attendance Management:** Provides attendance and payable-day information.
- **Leave Management:** Retrieves available leave balances.
- **Timesheet Queries:** Supports employee timesheet-related questions.
- **Conversational Interface:** Provides an interactive interface using Streamlit.

## Technology Stack
- Python
- LangChain
- FAISS Vector Database
- Hugging Face Embeddings
- Ollama (Qwen LLM)
- Streamlit
- Pandas
- Jupyter Notebook

## Project Structure

```text
HR-Chatbot/
│
├── app.py
├── hr_backend.py
├── HR_Chatbot.ipynb
├── data/
│   ├── Employee_Handbook.docx
│   └── HR_Data.xlsx
├── faiss_index/
└── .gitignore
```

## How It Works
1. HR documents are processed and divided into smaller text chunks.
2. Hugging Face embeddings convert text into numerical representations.
3. FAISS stores the embeddings for similarity-based retrieval.
4. LangChain connects the retrieval process with the language model.
5. Ollama runs the local Qwen language model.
6. Streamlit provides the user interface for interacting with the chatbot.
7. Structured employee information is retrieved from Excel datasets.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sapna-Chaudhary/HR-Chatbot.git
cd HR-Chatbot
```

### 2. Create a virtual environment

```bash
python -m venv hr_env
```

### 3. Activate the environment (Windows)

```bash
hr_env\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start Ollama

Install Ollama and pull the required Qwen model:

```bash
ollama pull qwen2.5:1.5b
```

### 6. Run the application

```bash
streamlit run app.py
```

## Learning Outcomes
- Working with Large Language Models (LLMs).
- Implementing Retrieval-Augmented Generation (RAG).
- Understanding vector databases and semantic search.
- Integrating structured and unstructured data.
- Building interactive applications using Streamlit.
- Working with local LLM deployments.

## Author
**Sapna Chaudhary**

GitHub: https://github.com/Sapna-Chaudhary
