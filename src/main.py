
from sklearn.metrics.pairwise import cosine_similarity
from reader import get_documents, get_requests, get_judgement
from cli import check_cli_args
from test import test_list
from tokenizer import tokenize
from vectorizer import Vectorizer

def eval(num_of_request=30):
  pass
  # Take the most_similar_docs in a list and compare the jugments 
  # -> judgements[request_index] -> list of {doc_id,is_related} compared to most_similar_docs 
  # This step will be done with 
  # return a pourcentage. 0.50 

def search(request_vectors, documents_vectors, preprocess_documents) : 
  cosine_similarities = cosine_similarity(request_vectors, documents_vectors)
  most_similar_docs_indices = cosine_similarities.argsort()[0][-5:]  # Adjust the number as needed
  most_similar_docs = [preprocess_documents[i] for i in most_similar_docs_indices]  # TODO HERE get the *title* and the content  
  return most_similar_docs_indices
 

def build_request_text(test,requests) :
  for request_index,(request_id,request_data) in enumerate(requests.items()) :
    request_string = request_data['title']
    if test.request_lenght=="long" : 
      request_string += " " + request_data['desc']
    request_data["text"] = request_string
  return requests

def run() :
  args=check_cli_args()
  # Get documents 
  documents_metadata = get_documents()  # print(documents_metadata[list(documents_metadata.keys())[0]].title)
 
  # Get requests
  requests = get_requests()

  # Get judgments
  judgements = get_judgement()  # print(judgements["2"])

  for test in test_list : 
    if(not args.test or args.test==test) : 
      vectorizer = Vectorizer(test.weight_schemat)
      print(test)

      # Tokenize docs
      preprocess_documents=tokenize(documents_metadata, test.pretreatment_type)
      # print("document_tokens length :", len(preprocess_documents))

      # Vectorize docs
      documents_vectors=vectorizer.vectorize(preprocess_documents, test.weight_schemat) # store vectors into database ? 
      # print(documents_vectors)

      # Tokenize requests, take in count the topic length (long our short)
      requests = build_request_text(test, requests)
      preprocess_requests=tokenize(requests, test.pretreatment_type) # print(preprocess_requests)

      # Vectorize requests
      for preprocess_request in preprocess_requests : 
        if("vectors" not in requests) : 
          requests['vectors'] = vectorizer.vectorize_request(preprocess_request, test.weight_schemat)
        # Search     
        indice = search(requests['vectors'], documents_vectors, preprocess_documents) # print(search_result)  
        print(preprocess_documents)  

      # Eval
      result=eval(num_of_request) 

      print("Result :", result)
     
      
if  __name__ == "__main__" : 
    run()


# def testing(): 
#   result = search("inverted index document")
#   print(result)

# def search(query):
 
#   query_vec = vectorizer.transform([query])
#   cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
#   related_docs_indices = cosine_similarities.argsort()[:-len(documents)-1:-1]
#   return related_docs_indices, cosine_similarities[related_docs_indices]

