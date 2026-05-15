import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Load data (replace with your CSV when available)
df = pd.read_csv("fulltrain.csv")  # <-- replace this with actual path

# Combine text fields for embedding
df["combined_text"] = df["Description"].fillna('') + " " + df["Close notes"].fillna('')

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(df["combined_text"].tolist(), show_progress_bar=True)

# Convert to numpy float32 array
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save index and metadata
faiss.write_index(index, "faiss_index.index")
with open("metadata.pkl", "wb") as f:
    pickle.dump(df.to_dict(orient="records"), f)

print("FAISS index and metadata saved.")
