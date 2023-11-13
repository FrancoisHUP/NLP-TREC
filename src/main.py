
from sklearn.metrics.pairwise import cosine_similarity
from reader import get_documents, get_requests, get_judgement
from cli import check_cli_args
from test import test_list
from tokenizer import tokenize
from vectorizer import Vectorizer
from evaluation import eval

number_document_retreive_per_request = 1000

def search(request_vectors, documents_vectors) : 
  cosine_similarities = cosine_similarity(request_vectors, documents_vectors)
  most_similar_docs_indices = cosine_similarities.argsort()[0][-number_document_retreive_per_request:]
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
  # qrels = readQrels() # 
  # qrels = parse_trec_file("TREC AP 88-90/TREC AP 88-90/jugements de pertinence/qrels.1-150.AP8890.txt") # TODO put in 3 seperate files ? 

  for test in test_list : 
    if(not args.test or args.test==test) : 
      vectorizer = Vectorizer(test.weight_schemat)
      print(test)

      # Tokenize docs
      preprocess_documents=tokenize(documents_metadata, test.pretreatment_type)  
      # print("document_tokens length :", preprocess_documents[0]['doc_id'])

      # Vectorize docs
      documents_vectors=vectorizer.vectorize([doc.get('token') for doc in preprocess_documents], test.weight_schemat) # store vectors into database ? 
      # print(documents_vectors)

      # Tokenize requests, take in count the topic length (long our short)
      requests = build_request_text(test, requests)
      preprocess_requests=tokenize(requests, test.pretreatment_type) # print(preprocess_requests)

      # Search results
      results={}
      for index, preprocess_request in enumerate(preprocess_requests,1) :
        # Vectorize requests 
        if("vectors" not in requests) : 
          requests['vectors'] = vectorizer.vectorize_request(preprocess_request, test.weight_schemat)
        # Search     
        most_similar_docs_indices = search(requests['vectors'], documents_vectors) 
        most_similar_docs = [preprocess_documents[i]["doc_id"] for i in most_similar_docs_indices] # for (index,most_similar_doc) in enumerate(most_similar_docs): print("DOCUMENTS ", index, " :", documents_metadata[most_similar_doc]["title"]) 
        results[index] = most_similar_docs

      # Eval
      metrics,MAP=eval(results,judgements) 

      print(test, "= result :", MAP, metrics)
     
      
if  __name__ == "__main__" : 
    run()
