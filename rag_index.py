import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

KNOWLEDGE_DIR = "knowledge"
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

documents = []
doc_texts = []

for file in os.listdir(KNOWLEDGE_DIR):
    path = os.path.join(KNOWLEDGE_DIR, file)
    with open(path, 'r') as f:
        text = f.read()
        documents.append(text)
        doc_texts.append(text)
        
embeddings = model.encode(doc_texts)
embeddings = np.array(embeddings).astype('float32')

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, 'rag.index')

with open('documents.txt', 'w', encoding='utf-8') as f:
    for doc in documents:
        f.write(doc.replace('\n', ' ') + '\n')