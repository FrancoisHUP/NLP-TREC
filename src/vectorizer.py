from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
# from rank_bm25 import BM25Okapi
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
from multiprocessing import Pool
from scipy.sparse import vstack

def search(request_vectors, documents_vectors, number_document_retreive) : 
  cosine_similarities = cosine_similarity(request_vectors, documents_vectors)
  most_similar_docs_indices = cosine_similarities.argsort()[0][-number_document_retreive:]
  return most_similar_docs_indices

class Vectorizer: 

    def __init__(self, weight_scheme):
        self.weight_scheme = weight_scheme
        self.vectorizer = None
        if weight_scheme == 'normalized_frequency':
          self.vectorizer=CountVectorizer()
        if weight_scheme == 'tf_idf_normalize':
          self.vectorizer = TfidfVectorizer(max_features=10000,  # Limit the number of features
                                            min_df=0.01,         # Ignore terms with low document frequency
                                            max_df=0.7)          # Ignore terms with very high document frequency

    def _vectorize_chunk(self, chunk):
      # This method will be run in a separate process
      if self.weight_scheme == 'tf_idf_normalize':
        return self.vectorizer.transform(chunk)
      if self.weight_scheme == 'normalized_frequency':
        normalize_frequency = self.vectorizer.transform(chunk)
        return normalize(normalize_frequency, norm='l1', axis=1)
      else:
        raise ValueError("Unsupported vectorization method for multiprocessing")

    def vectorize(self, documents, n_processes=4):
      # Extract document texts and convert to a list
      document_texts = [doc for doc in documents]

      # Split document texts into chunks
      chunk_size = len(document_texts) // n_processes
      chunks = [document_texts[i:i + chunk_size] for i in range(0, len(document_texts), chunk_size)]

      # Initialize the vectorizer (if not already done)
      if not self.vectorizer or not hasattr(self.vectorizer, 'vocabulary_'):
          self.vectorizer.fit(document_texts)

      # Use multiprocessing to vectorize each chunk
      with Pool(processes=n_processes) as pool:
          results = pool.map(self._vectorize_chunk, chunks)

      # Combine results from all processes
      return vstack(results)  # vstack is used for combining sparse matrices

