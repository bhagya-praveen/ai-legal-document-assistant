import numpy as np
from google import genai

from config import Config


client = genai.Client(
    api_key=Config.GEMINI_API_KEY
)


def create_embedding(text):
    """
    Convert text into a numerical vector using Gemini.
    """

    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )

    return np.array(response.embeddings[0].values)


def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.
    """

    denominator = (
        np.linalg.norm(vector_a) *
        np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0

    return np.dot(vector_a, vector_b) / denominator