<h1 align="center">AI DOCUMENT ASSISTANT</h1>
<h3 align="center">Ask Questions and get Answers Instantly</h3>


<img width="1858" height="968" alt="qna" src="https://github.com/user-attachments/assets/8a5f652d-c21d-4f06-8b4f-9aed9c601f8f" />



## What it does
Most businesses sit on a goldmine of information locked inside PDFs, reports, and contracts that nobody has time to read. This app lets you upload any document and simply ask it questions in plain language. 

You get instant, accurate answers along with the exact source it pulled the information from,

## Live Demo


## Real World Use Cases
- A business owner analyzing client reports
- A law firm searching through contracts instantly
- An HR team querying internal policies
- A person searching for information in their personal docs


## What makes it valuable
- reduce search time from hours to seconds
- seach multiple documets simultaneously
- get answers with the exact sources they were pulled from

## Tech Stack
- **Frontend**: React
- **Backend API**: Python FastAPI
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI Embedding Model
- **Query Engine**: LlamaIndex
- **RAG Pipeline**: Custom retrieval-augmented generation implementation


## Run Locally
1. Clone the repository
```bash
git clone https://github.com/amvvr1/QnA-APP.git
cd qna-app
```

2. Install frontend dependencies
```bash
cd frontend
npm install
```

3. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

4. Set up environment variables
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

5. Run the application
```bash
#start the backend (from backend directory)
uvicorn app.main:app --reload

# Start frontend (from frontend directory)
npm start
```

## Contact
**Email:**  scholarammar@gmail.com


