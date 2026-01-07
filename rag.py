import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

index = faiss.read_index("rag.index")

with open("documents.txt", "r", encoding="utf-8") as f:
    documents = f.readlines()

def retrieve_context(query: str, k: int = 2):
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, k)

    results = []
    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])

    return "\n".join(results)
