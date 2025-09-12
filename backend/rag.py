import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import subprocess
import json
from PyPDF2 import PdfReader


class RAG:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.text_chunks = []

    def add_documents(self, texts):
        self.text_chunks.extend(texts)
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        d = embeddings.shape[1]

        if self.index is None:
            self.index = faiss.IndexFlatL2(d)
            self.index.add(embeddings)
        else:
            self.index.add(embeddings)

    def process_file(self, file_path: str):
        """Reads a PDF or text file and indexes its contents"""
        if file_path.lower().endswith(".pdf"):
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        # Split by paragraphs
        chunks = [chunk.strip() for chunk in text.split("\n") if chunk.strip()]
        self.add_documents(chunks)

    def query(self, question: str, top_k=3):
        if self.index is None or len(self.text_chunks) == 0:
            return "No documents uploaded yet.", []

        # Step 1: Retrieve relevant chunks
        q_emb = self.model.encode([question])
        distances, indices = self.index.search(q_emb, top_k)
        sources = [self.text_chunks[i] for i in indices[0]]

        # Step 2: Build prompt
        context = "\n\n".join(sources)
        prompt = f"""
        Use the context below to answer the question. Be concise.

        Context:
        {context}

        Question: {question}
        """

        # Step 3: Run Ollama model (mistral)
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
        )
        answer = result.stdout.decode("utf-8").strip()

        return answer, sources
