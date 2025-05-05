# utils.py

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load models
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
t5_model = T5ForConditionalGeneration.from_pretrained('t5-small')
t5_tokenizer = T5Tokenizer.from_pretrained('t5-small')

# Load documents from a file (one block per question/answer pair)
def load_documents(file_path='E:/Spring_2025/CapstoneProject/13th April 2025______Final/Personal Projects/AI-Powered_Knowledge_Base_with_Dynamic_Answer_Generation/data/documents.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        blocks = f.read().strip().split('\n\n')
        return [block.replace('\n', ' ').strip() for block in blocks if block.strip()]

documents = load_documents()

# Compute document embeddings
document_embeddings = embedding_model.encode(documents, convert_to_numpy=True).astype('float32')

# Initialize FAISS
index = faiss.IndexFlatL2(document_embeddings.shape[1])
index.add(document_embeddings)

# Encode text into embeddings
def encode_text(texts):
    embeddings = embedding_model.encode(texts, convert_to_numpy=True)
    return np.array(embeddings).astype('float32')

# Retrieve top 3 documents using FAISS
def search(query):
    query_embedding = encode_text([query])
    _, indices = index.search(query_embedding, k=3)
    return [documents[i] for i in indices[0]]

# Generate answer using T5
def generate_answer(query, context):
    input_text = f"question: {query} context: {context}"
    inputs = t5_tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = t5_model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])
    answer = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer
