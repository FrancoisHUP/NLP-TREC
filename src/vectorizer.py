from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from rank_bm25 import BM25Okapi
from sklearn.preprocessing import normalize
import numpy as np

class Vectorizer: 

  def __init__(self, weight_scheme):
    self.vectorizer=None
    if weight_scheme == 'normalized_frequency':
      self.vectorizer=CountVectorizer()
    if weight_scheme == 'tf_idf_normalize':
      self.vectorizer=TfidfVectorizer()
    if weight_scheme == 'BM25': # TODO check
      self.vectorizer=BM25Okapi()

  def vectorize(self, preprocess_documents, weight_scheme):
    documents = [preprocess_documents] if isinstance(preprocess_documents, str) else preprocess_documents
    if weight_scheme == 'normalized_frequency':
      # Apply the vectorizer on the documents
      normalize_frequency = self.vectorizer.fit_transform(documents)
      # Normalize the frequency vectors
      return normalize(normalize_frequency, norm='l1', axis=1)
    if weight_scheme == 'tf_idf_normalize':
      # Convert a collection of raw documents to a matrix of TF-IDF features.
      return self.vectorizer.fit_transform(documents)
    if weight_scheme == 'BM25':
      # Tokenize documents for BM25
      tokenized_docs = [doc.split(" ") for doc in documents]
      bm25 = BM25Okapi(tokenized_docs)
      return bm25
    else:
      raise ValueError("Unknown vectorization method")

  def vectorize_request(self, preprocess_request_string, weight_scheme):
    request = [preprocess_request_string] if isinstance(preprocess_request_string, str) else preprocess_request_string
    if weight_scheme == 'normalized_frequency':
      # Apply the vectorizer on the documents
      normalize_frequency = self.vectorizer.transform(request)
      # Normalize the frequency vectors
      return normalize(normalize_frequency, norm='l1', axis=1)
    if weight_scheme == 'tf_idf_normalize':
      # Convert a collection of raw documents to a matrix of TF-IDF features.
      return self.vectorizer.transform(request)
    if weight_scheme == 'BM25':
      # Tokenize documents for BM25
      tokenized_docs = [doc.split(" ") for doc in request]
      bm25 = BM25Okapi(tokenized_docs)
      return bm25
    else:
      raise ValueError("Unknown vectorization method")
    