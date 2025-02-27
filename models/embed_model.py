from sentence_transformers import SentenceTransformer
from config.settings import MODEL_NAME

# Load Model
model = SentenceTransformer(MODEL_NAME)
