from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sample documents
documents = [
    "Natural language processing enables computers to understand human language.",
    "An inverted index allows efficient document retrieval.",
    "Building an inverted index involves tokenizing documents."
]

# Create a TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# Vectorize the documents
tfidf_matrix = vectorizer.fit_transform(documents)

# Function to perform search
def search(query):
    query_vec = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-len(documents)-1:-1]
    return related_docs_indices, cosine_similarities[related_docs_indices]

# Example search
print(search("inverted index document"))