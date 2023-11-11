
from reader import get_documents
from cli import check_cli_args
from test import test_list
from tokenizer import Tokenizer
from vectorizer import Vectorizer

def run() :
  args=check_cli_args()
  tokenizer = Tokenizer()
  vectorizer = Vectorizer()

  #TESTS
  if(args.test) :
    print("run ",  args.test)
  else: 
    print("run : all test")
  
  # Get documents 
  documents_metadata = get_documents()
  # print(documents_metadata[list(documents_metadata.keys())[0]].title)

  for test in test_list : 
    if(not args.test or args.test==test) : 

      # Tokenize docs
      inverted_index_tokens=tokenizer.tokenize(documents_metadata, test.pretreatment_type)
      # print("document_tokens :", inverted_index_tokens)

      # Vectorize docs
      document_vectorize=vectorizer.vectorize(document_tokens) 
      # tfidf_vectorizer = TfidfVectorizer()
      # tfidf_matrix = tfidf_vectorizer.fit_transform(processed_texts, test.weight_schemat)


if  __name__ == "__main__" : 
    run()













# result=test(test.pretreatment_type,test.weight_schemat, test.request_lenght)
# def test(pretreatment_type="none", weight_schemat="normalized_frequency", request_lenght="short") : 
#   """
#   Parameters
#   ----------
#     pretreatment_type : str 
#       The type of pretreatment -> "none" or "lemmatization" or "steaming"
#     weight_schemat : string
#       The weighting shema -> "normalized_frequency" or "Tf_idf_normalize" or  "Okapi_BM25"
#     request_lenght : str
#         The request lenght ->  "short" or "long",
#   """
  # runTests()
  # outputFile() 