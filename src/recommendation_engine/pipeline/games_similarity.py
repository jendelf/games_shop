from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
from src.settings import settings
import numpy as np

# в будущем для улучшения рекомендаций если пользователь добавляет игру в избранное
def get_games_similarity():
    tfidf_matrix = load_npz(settings.MODEL_DIR / "tfidf_matrix.npz")
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    np.save(settings.MODEL_DIR / "similarity_matrix.npy", similarity_matrix)

