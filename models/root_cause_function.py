# Load model
import pickle
import river
with open("models/root_cause_model_final.pkl", "rb") as f:
    clf = pickle.load(f)

encoding_labels = ['Core Application Functionality Issues',
    'Data Integrity & Synchronization Errors',
    'Information & Documentation Gaps', 'Miscellaneous/Uncategorized',
    'Network Connectivity & Performance Issues',
    'Order Management Issues', 'Payment & Billing Discrepancies',
    'Platform & Infrastructure Failures',
    'Process & Workflow Breakdowns',
    'Product & Service Specific Defects',
    'User Authentication & Authorization Issues',
    'User Interface (UI) & User Experience (UX) Glitches']
from sentence_transformers import SentenceTransformer
import numpy as np

# Load the model once
embedder = SentenceTransformer("all-MiniLM-L6-v2")
def predict_root_cause(full_text):
    vec = embedder.encode(full_text)
    x = {f"dim_{i}": float(val) for i, val in enumerate(vec)}

    y_pred = clf.predict_one(x)
    index = float(y_pred)
    index = int(index)
    return encoding_labels[index]
st_model = SentenceTransformer("all-MiniLM-L6-v2")

# Define the embedding function to convert text to river-compatible dict
def embed_func(text):
    vec = st_model.encode(text)
    return {f"dim_{i}": float(v) for i, v in enumerate(vec)}


def update_and_verify(text, predicted_label, true_label):
    x = embed_func(text)
    clf.learn_one(x, str(true_label))  # Update model with true label
    new_pred = clf.predict_one(x)  # Predict again after update
    return new_pred[0], true_label

# print(update_and_verify("Keyboard is not responding on network","Miscellaneous/Uncategorized","Product & Service Specific Defects"))