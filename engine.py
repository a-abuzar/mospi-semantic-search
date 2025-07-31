import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path

def create_search_engine():
    """
    Builds the search engine using the state-of-the-art E5 multilingual model.
    """
    data_path = Path('data')
    app_path = Path('app')
    app_path.mkdir(exist_ok=True)

    # 1. Load the clean dataset
    csv_file = data_path / 'nco_data.csv'
    if not csv_file.exists():
        print(f"FATAL ERROR: The file {csv_file} was not found. Please run parser.py first.")
        return
        
    print("Loading the clean NCO dataset...")
    df = pd.read_csv(csv_file)
    df.dropna(subset=['description'], inplace=True)

    # 2. --- E5 MODEL UPGRADE ---
    # Prepend the 'passage: ' prefix to each description for optimal E5 performance.
    print("Prepending 'passage:' prefix to all descriptions for E5 model.")
    df['description_for_embedding'] = 'passage: ' + df['description']
    descriptions = df['description_for_embedding'].tolist()

    # Load the E5 model
    model_name = 'intfloat/multilingual-e5-large'
    print(f"Loading SOTA model: {model_name}")
    model = SentenceTransformer(model_name)

    # 3. Generate embeddings
    print(f"Generating E5 embeddings for {len(descriptions)} descriptions.")
    embeddings = model.encode(descriptions, show_progress_bar=True, convert_to_numpy=True)
    print("Embeddings generated successfully.")

    # 4. Build the FAISS index
    dimension = embeddings.shape[1]
    print(f"Building FAISS index with dimension {dimension}...")
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print(f"FAISS index built. Total entries indexed: {index.ntotal}")

    # 5. Save the essential components
    index_path = app_path / 'index.faiss'
    lookup_path = app_path / 'lookup_data.csv'
    
    print(f"Saving FAISS index to {index_path}")
    faiss.write_index(index, str(index_path))

    # Save the original descriptions without the prefix for display purposes
    print(f"Saving lookup data to {lookup_path}")
    df[['nco_code', 'description']].to_csv(lookup_path, index=False, encoding='utf-8')

    print("\n--- E5 AI ENGINE BUILD COMPLETE ---")

if __name__ == '__main__':
    create_search_engine()