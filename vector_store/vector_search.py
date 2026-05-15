import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Base path = directory of this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Correct paths regardless of where you run the script
INDEX_PATH = os.path.join(BASE_DIR, "faiss_index.index")
META_PATH = os.path.join(BASE_DIR, "metadata.pkl")

# Load index and metadata
index = faiss.read_index(INDEX_PATH)
with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_similar_cases(user_input, top_k=5):
    query_embedding = model.encode([user_input]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "rank": i+1,
            "distance": float(distances[0][i]),
            "ticket": metadata[idx]
        })
    return results

# query = "Orders not showing complete status in POS system"
# similar = search_similar_cases(query)

# for case in similar:
#     print(f"Rank: {case['rank']}, Distance: {case['distance']}")
#     print(f"Description: {case['ticket']['Description']}")
#     print(f"Root Cause: {case['ticket']['root_cause']}")
#     print("=" * 50)