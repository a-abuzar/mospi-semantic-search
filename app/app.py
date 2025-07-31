from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path

# --- 1. Initialization ---
app = Flask(__name__)
app_path = Path(__file__).parent

# --- 2. Load the E5 AI Engine Components ---
print("Loading the E5 AI search engine components...")

# --- E5 MODEL UPGRADE ---
model_name = 'intfloat/multilingual-e5-large'

try:
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)
    print("E5 model loaded.")

    index_path = app_path / 'index.faiss'
    index = faiss.read_index(str(index_path))
    print(f"FAISS index loaded. Contains {index.ntotal} vectors.")

    lookup_path = app_path / 'lookup_data.csv'
    lookup_df = pd.read_csv(lookup_path)
    print("Lookup data loaded.")

    ENGINE_READY = True
except Exception as e:
    print(f"FATAL ERROR: Could not load AI engine components. {e}")
    ENGINE_READY = False

# --- 3. Define the Search Function ---
def search_occupations(query_text, k=5):
    if not ENGINE_READY:
        return []
    
    # --- E5 MODEL UPGRADE ---
    # Prepend the 'query: ' prefix to the user's query for optimal E5 performance.
    query_for_embedding = 'query: ' + query_text
    
    query_embedding = model.encode([query_for_embedding], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, k)
    results = lookup_df.iloc[indices[0]].to_dict(orient='records')
    return results

# --- 4. Define Web Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_query = request.form.get('query', '')
    if user_query:
        search_results = search_occupations(user_query)
        return render_template('index.html', results=search_results, query=user_query)
    return render_template('index.html')

# --- 5. Run the Application ---
if __name__ == '__main__':
    app.run(debug=True)