import numpy as np
from scipy.sparse import load_npz
from sklearn.neighbors import NearestNeighbors
from src.settings import settings

def get_games_top_similar(top_k=15):
    tfidf_matrix = load_npz(settings.MODEL_DIR / "tfidf_matrix.npz")
    nn = NearestNeighbors(n_neighbors=top_k+1, metric='cosine', algorithm='brute') # there top_k+1 because KNN returns the current object with distance zero
    nn.fit(tfidf_matrix)
    
    distances, indices = nn.kneighbors(tfidf_matrix)

    top_similar = []
    for idx_list, dist_list in zip(indices, distances):
        sim_list = [(i, 1 - d) for i, d in zip(idx_list[1:], dist_list[1:])]  # exclude the current object
        top_similar.append(sim_list)
    
    np.save(settings.MODEL_DIR / "top_similar_games.npy", top_similar)
