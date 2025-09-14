# AI-Knowledge-Base
📚 AI Knowledge Base

A full-stack Retrieval-Augmented Generation (RAG) application that lets users upload PDFs/TXT files and query them in natural language. The system retrieves relevant context and generates grounded answers with cited sources using Ollama LLMs (Mistral).

✨ Features

🔍 Semantic Search — Uses FAISS + Sentence Transformers to embed and retrieve the most relevant text chunks.

🤖 LLM Integration — Contextual prompting pipeline with Ollama (Mistral) for concise, grounded answers.

📂 File Uploads — Users can upload .pdf or .txt documents for indexing and querying.

🖥️ Full-Stack Implementation

Backend: FastAPI with endpoints for file processing, embeddings indexing, and Q&A.

Frontend: Next.js + Tailwind for a clean, interactive UI.

📑 Transparent Responses — Answers include source text snippets for credibility.

🛠 Tech Stack

Backend: FastAPI, FAISS, Sentence Transformers, Ollama

Frontend: Next.js, React, Tailwind CSS, Axios

Other: PDF/Text parsing, CORS-enabled API

🚀 How It Works

Upload a .pdf or .txt file.

The backend extracts content, splits it into chunks, and indexes embeddings with FAISS.

Ask a question in natural language.

The app retrieves the top-k relevant chunks and passes them to Ollama for answer generation.

The UI displays the answer with cited sources.
