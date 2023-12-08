# def vectorize_request(self, preprocess_request_string, weight_scheme, ):
#   request = [preprocess_request_string] if isinstance(preprocess_request_string, str) else preprocess_request_string
#   if weight_scheme == 'normalized_frequency':
#     # Apply the vectorizer on the documents
#     normalize_frequency = self.vectorizer.transform(request)
#     # Normalize the frequency vectors
#     return normalize(normalize_frequency, norm='l1', axis=1)
#   if weight_scheme == 'tf_idf_normalize':
#     # Convert a collection of raw documents to a matrix of TF-IDF features.
#     return self.vectorizer.transform(request)
#   if weight_scheme == 'BM25':
#     # Tokenize documents for BM25
#     tokenized_docs = [doc.split(" ") for doc in request]
#     bm25 = BM25Okapi(tokenized_docs)
#     return bm25
#   else:
#     raise ValueError("Unknown vectorization method")




# # # Example usage
# results = [['AP880212-0125', 'AP880216-0139', 'AP880213-0106', 'AP880213-0105', 'AP880216-0169'], ['AP880212-0125', 'AP880216-0139', 'AP880213-0106', 'AP880216-0221', 'AP880216-0169']]
# judgments = {
#     '1': [{'doc_id': 'AP880212-0125', 'is_related': False}, {'doc_id': 'AP880212-0161', 'is_related': False}, {'doc_id': 'AP880216-0139', 'is_related': True}, {'doc_id': 'AP880216-0169', 'is_related': True}, {'doc_id': 'AP880217-0026', 'is_related': False}, {'doc_id': 'AP880217-0030', 'is_related': False}],
#     '2': [{'doc_id': 'AP880212-0125', 'is_related': True}, {'doc_id': 'AP880212-0126', 'is_related': False}, {'doc_id': 'AP880212-0128', 'is_related': False}, {'doc_id': 'AP880212-0161', 'is_related': False}, {'doc_id': 'AP880212-0162', 'is_related': True}, {'doc_id': 'AP880216-0221', 'is_related': True}]
# }

# # Calculate MAP
# map_metric = calculate_map(results, judgments)
# print(map_metric)



# def calculate_map(results, judgements): 
#     average_precisions = []
#     for request_id, judgement_docs in judgements.items():
#         results_docs = results.get(int(request_id)) # result_of_request_x
#         cum_relevant = 0
#         precision_sum = 0
#         for i, doc_id in enumerate(judgement_docs, 1):
#           if doc_id in results_docs:
#             cum_relevant += 1
#             precision_sum += cum_relevant / i
#         average_precision = precision_sum / len(results_docs) if results_docs else 0
#         average_precisions.append(average_precision)
#     return sum(average_precisions) / len(average_precisions) if average_precisions else 0


 # def vectorize(self, preprocess_documents, transform=False):
  #     documents = [preprocess_documents] if isinstance(preprocess_documents, str) else preprocess_documents

  #     # Initialize progress bar
  #     progressBar(documents, prefix='[VECTORIZE ]', suffix='Complete', length=50)

  #     if self.weight_scheme == 'normalized_frequency' or self.weight_scheme == 'tf_idf_normalize':
  #         # Apply the vectorizer on the documents
  #         for i, doc in enumerate(documents):
  #             normalize_frequency=None
  #             if len(doc) > 10:
  #               if(transform): 
  #                 self.vectorizer.transform([doc])
  #               else : 
  #                 normalize_frequency = self.vectorizer.fit_transform([doc])
  #               # Update progress for each document
  #               yield normalize(normalize_frequency, norm='l1', axis=1)
  #               progressBar(documents, prefix='[VECTORIZE ]', suffix='Complete', length=50)

  #     elif self.weight_scheme == 'BM25':
  #         # Tokenize documents for BM25
  #         tokenized_docs = [doc.split(" ") for doc in documents]
  #         bm25 = BM25Okapi(tokenized_docs)
  #         return bm25
  #     else:
  #         raise ValueError("Unknown vectorization method")




# def tokenize(documents_metadata, pretreatment_type):
#     stop_words = set(stopwords.words('english'))
#     stemmer = PorterStemmer()
#     lemmatizer = WordNetLemmatizer()

#     preprocess_documents = []
#     with ThreadPoolExecutor() as executor:
#         futures = [executor.submit(process_document, data, pretreatment_type, stop_words, stemmer, lemmatizer, doc_id)
#                    for doc_id, data  in progressBar(documents_metadata.items(), prefix = '[TOKENIZE ]', suffix = 'Complete', length = 50)]

#         for future in futures:
#             preprocess_documents.append(future.result())

#     return preprocess_documents

# def tokenize(documents_metadata, pretreatment_type):
#     stop_words = set(stopwords.words('english'))
#     stemmer = PorterStemmer()
#     lemmatizer = WordNetLemmatizer()

#     preprocess_documents = []
    
#     for doc_id, data  in progressBar(documents_metadata.items(), prefix = '[TOKENIZE ]', suffix = 'Complete', length = 50):
#     # for doc_id, data in documents_metadata.items():
#         if "tokens" not in data:
#             data["tokens"] = word_tokenize(data["text"].lower())

#         if pretreatment_type == "basic":
#             if "basic_token" not in data:
#                 data['basic_token'] = ' '.join(data["tokens"])
#             preprocess_documents.append({"token":data['basic_token'],"doc_id":doc_id})

#         elif pretreatment_type == "lemmatization":
#             if "lemme_token" not in data:
#                 lemme_token = [lemmatizer.lemmatize(token) for token in data["tokens"] if token not in stop_words]
#                 data['lemme_token'] = ' '.join(lemme_token)
#             preprocess_documents.append(data['lemme_token'])

#         elif pretreatment_type == "stemming":
#             if "stemme_token" not in data:
#                 stemme_token = [stemmer.stem(token) for token in data["tokens"] if token not in stop_words]
#                 data['stemme_token'] = ' '.join(stemme_token)
#             preprocess_documents.append(data['stemme_token'])

#         else:
#             raise ValueError("Unknown tokenisation method")

#     return preprocess_documents
        
# def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
#     """
#     Call in a loop to create terminal progress bar
#     @params:
#         iterable    - Required  : iterable object (Iterable)
#         prefix      - Optional  : prefix string (Str)
#         suffix      - Optional  : suffix string (Str)
#         decimals    - Optional  : positive number of decimals in percent complete (Int)
#         length      - Optional  : character length of bar (Int)
#         fill        - Optional  : bar fill character (Str)
#         printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
#     """
#     total = len(iterable)
#     # Progress Bar Printing Function
#     def printProgressBar (iteration):
#         percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
#         filledLength = int(length * iteration // total)
#         bar = fill * filledLength + '-' * (length - filledLength)
#         print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
#     # Initial Call
#     printProgressBar(0)
#     # Update Progress Bar
#     for i, item in enumerate(iterable):
#         yield item
#         printProgressBar(i + 1)
#     # Print New Line on Complete
#     print()

      

# def vectorize(self, preprocess_documents, weight_scheme):
#   documents = [preprocess_documents] if isinstance(preprocess_documents, str) else preprocess_documents
#   total_docs = len(documents)

#   # Progress Bar Initialization
#   for i, doc in progressBar(range(total_docs), prefix = 'Vectorizing:', suffix = 'Complete', length = 50):
#       if weight_scheme == 'normalized_frequency':
#           # Apply the vectorizer on the document
#           normalize_frequency = self.vectorizer.fit_transform([doc])
#           # Normalize the frequency vectors
#           yield normalize(normalize_frequency, norm='l1', axis=1)
#       elif weight_scheme == 'tf_idf_normalize':
#           # Convert a collection of raw documents to a matrix of TF-IDF features.
#           yield self.vectorizer.fit_transform([doc])
#       elif weight_scheme == 'BM25':
#           # Tokenize document for BM25
#           tokenized_doc = doc.split(" ")
#           bm25 = BM25Okapi([tokenized_doc])
#           yield bm25
#       else:
#           raise ValueError("Unknown vectorization method")


# Usage
# documents = get_documents()
# vectorizer = Vectorizer('tf_idf_normalize')
# vectorized_documents = vectorizer.vectorize(documents, n_processes=4)
# print("done")


# class Vectorizer: 

#   def __init__(self, weight_scheme):
#     self.weight_scheme=weight_scheme
#     self.vectorizer=None
#     if weight_scheme == 'normalized_frequency':
#       self.vectorizer=CountVectorizer()
#     if weight_scheme == 'tf_idf_normalize':
#       self.vectorizer=TfidfVectorizer()
#     if weight_scheme == 'BM25': # TODO check
#       self.vectorizer=BM25Okapi()

#   def vectorize(self, preprocess_documents, transform=False):
#       documents = [preprocess_documents] if isinstance(preprocess_documents, str) else preprocess_documents
#       if self.weight_scheme == 'normalized_frequency':
#         if(transform) : 
#           normalize_frequency = self.vectorizer.transform(documents)
#         else :
#           # Apply the vectorizer on the documents
#           normalize_frequency = self.vectorizer.fit_transform(documents)
#         # Normalize the frequency vectors
#         return normalize(normalize_frequency, norm='l1', axis=1)
#       if self.weight_scheme == 'tf_idf_normalize':
#         if(transform) : 
#           return self.vectorizer.transform(documents)
#         else : 
#           # Convert a collection of raw documents to a matrix of TF-IDF features.
#           return self.vectorizer.fit_transform(documents)
#       if self.weight_scheme == 'BM25': # TODO 
#         # Tokenize documents for BM25
#         tokenized_docs = [doc.split(" ") for doc in documents]
#         bm25 = BM25Okapi(tokenized_docs)
#         return bm25
#       else:
#         raise ValueError("Unknown vectorization method")



from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, QueryParser
from org.apache.lucene.queryparser.classic import QueryParser

def create_index(index_dir, documents):
    # Create a directory to store the index
    store_dir = SimpleFSDirectory(Paths.get(index_dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    writer = IndexWriter(store_dir, config)

    for doc in documents:
        lucene_doc = Document()
        lucene_doc.add(TextField("content", doc, Field.Store.YES))
        writer.addDocument(lucene_doc)

    writer.close()

def search_index(index_dir, query_str):
    # Open the directory containing the index
    store_dir = SimpleFSDirectory(Paths.get(index_dir))
    reader = DirectoryReader.open(store_dir)
    searcher = IndexSearcher(reader)
    analyzer = StandardAnalyzer()

    query = QueryParser("content", analyzer).parse(query_str)
    hits = searcher.search(query, 10).scoreDocs

    results = []
    for hit in hits:
        doc_id = hit.doc
        doc = searcher.doc(doc_id)
        results.append(doc.get("content"))

    reader.close()
    return results

# Define some documents
documents = [
    "Hello world",
    "PyLucene is a Python extension for Lucene",
    "Lucene is a powerful text search engine"
]

# Indexing the documents
index_dir = "/index"  # Change this to a valid path on your system
create_index(index_dir, documents)

# Searching the index
query_str = "Lucene"
search_results = search_index(index_dir, query_str)

print("Search Results for '{}':".format(query_str))
for result in search_results:
    print(result)


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



# results={}
      # for index,request_vectors in enumerate(requests_vectors, 1) : 
      #   if index < max_request : 
      #     most_similar_docs_indices = search(request_vectors, documents_vectors, number_document_retreive) 
      #     most_similar_docs = [preprocess_documents[i]["doc_id"] for i in most_similar_docs_indices] # for (index,most_similar_doc) in enumerate(most_similar_docs): print("DOCUMENTS ", index, " :", documents_metadata[most_similar_doc]["title"]) 
      #     results[index] = most_similar_docs
# avg_precision, avg_recall, map_score=eval(results,judgements) 



  # Get judgments
  # print("[LOAD] judgments")
  # judgements = get_judgement()  # print(judgements["2"])