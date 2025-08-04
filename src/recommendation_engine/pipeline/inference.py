from sklearn.metrics.pairwise import cosine_similarity
from src.settings import settings
import numpy as np

def inference(user_vector, top_k):
    similarity_matrix = np.load(settings.MODEL_DIR / "similarity_matrix.npy")
    user_vector = np.array(user_vector)
    if user_vector.ndim == 1:
        user_vector = user_vector.reshape(1, -1)
    recommendation = cosine_similarity(similarity_matrix, user_vector)
    recommendation = recommendation.flatten()
    top_indices = recommendation.argsort()[::-1][:top_k]
    return top_indices
