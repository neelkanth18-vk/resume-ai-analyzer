import numpy as np
from typing import Optional

# We wrap the import in a try-except so the app doesn't crash if it's still downloading
try:
    from sentence_transformers import SentenceTransformer
    # all-MiniLM-L6-v2 is extremely fast and provides great semantic accuracy for english text
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Warning: Failed to load SentenceTransformer: {e}")
    model = None

def compute_semantic_similarity(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity between two texts.
    Returns a float between 0.0 and 1.0.
    """
    if not model or not text1 or not text2:
        return 0.0
        
    try:
        embeddings = model.encode([text1, text2])
        emb1 = embeddings[0]
        emb2 = embeddings[1]
        
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        similarity = dot_product / (norm1 * norm2)
        
        # Clip between 0 and 1 (cosine similarity ranges -1 to 1)
        return float(max(0.0, min(1.0, similarity)))
    except Exception as e:
        print(f"Error computing similarity: {e}")
        return 0.0
