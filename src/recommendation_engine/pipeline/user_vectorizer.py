from typing import List, Optional
from .feature_extraction import answers_vectorizer

def build_user_vector(game_mode: str, genres: List[str], favourites: str, genres_other: Optional[str]):
    genres_text = " ".join(genres)
    other_genres = " ".join(s.strip().lower() for s in genres_other.split(",")) if genres_other else ""
    combined_text = f"{game_mode} {genres_text} {favourites} {other_genres or ''}".strip()
    return answers_vectorizer(combined_text, 0, 0)