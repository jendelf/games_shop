from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pickle
from scipy.sparse import hstack,save_npz

from src.settings import settings
from src.utils.data_preprocessing import recommendation_df_preprocess

def extract_df_features():
    df = recommendation_df_preprocess()

    numeric_cols = ['positive_ratings', 'negative_ratings']
    text_col = 'processed_text'

    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    text_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent', fill_value='')),
        ('vectorizer', TfidfVectorizer(
            ngram_range=settings.NGRAM_RANGE,
            max_features=settings.MAX_FEATURES,
        ))
    ])

    preprocessor = ColumnTransformer([
        ('num', num_pipeline, numeric_cols),
        ('text', text_pipeline, text_col)
    ])

    combined_features = preprocessor.fit_transform(df)

    settings.MODEL_DIR.mkdir(exist_ok=True, parents=True)

    with open(settings.MODEL_DIR / "preprocessor.pkl", "wb") as f:
        pickle.dump(preprocessor, f)

    save_npz(settings.MODEL_DIR / "features_matrix.npz", combined_features)

    return combined_features, df

def answers_vectorizer(processed_text, positive_rating = 0, negative_rating = 0):
    with open(settings.MODEL_DIR / "preprocessor.pkl", "rb") as f:
        preprocessor = pickle.load(f)

    scaler = preprocessor.named_transformers_['num'].named_steps['scaler']
    tf_vectorizer = preprocessor.named_transformers_['text'].named_steps['vectorizer'] #tf-idf vectorizer
    #transform new input
    numerical = scaler.transform([[positive_rating, negative_rating]])
    tf_idf = tf_vectorizer.transform([processed_text])
    combined = hstack([numerical,tf_idf])
    return combined
