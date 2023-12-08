
from reader import get_documents, get_requests, get_judgement
from cli import check_cli_args
from test import test_list
from tokenizer import tokenize, tokenize_no_mp
from vectorizer import Vectorizer #, search
from index_lucene import indexing, search
from evaluation import trec_eval
from writer import write_run_file, write_result
import glob
import datetime
import os
import shutil

#P@100
# number_document_retreive = 100
# Tested on max_request amout of request
# max_request = 30


def delete_directory_contents(dir_path):
    # Check if the directory exists
    if not os.path.isdir(dir_path):
        print("Directory does not exist:", dir_path)
        return

    # Iterate over all the files and directories in the given directory
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        
        try:
            # If it's a file or a link, delete it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # If it's a directory, delete its contents recursively
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def build_request(test, requests) :
  for request_index,(request_id,request_data) in enumerate(requests.items()) :  
    request_string = request_data['title']
    if test.request_lenght=="long" : 
      request_string += " " + request_data['desc']
    request_data["text"] = request_string

def format_res(overall_result) :
  map_values = [inner_dict['map'] for inner_dict in overall_result.values()]
  mean_map = sum(map_values) / len(map_values)
  P_10 = [inner_dict['P@10'] for inner_dict in overall_result.values()]
  mean_P_10 = sum(P_10) / len(P_10)
  # 5, 10, 15, 20, 30, 100, 200, 500, 1000
  return { 
    "MMAP" : mean_map, 
    "P@10" :mean_P_10,
    "num_ret": overall_result["1"]["num_ret"], 
    "num_rel": overall_result["1"]["num_rel"],
    "num_rel_ret" : overall_result["1"]["num_rel_ret"],
  }

def run() :
  args=check_cli_args()

  # Get documents 
  print(datetime.datetime.now(), "[LOAD] documents")#, end=', ')
  documents_metadata = get_documents()  # print(documents_metadata[list(documents_metadata.keys())[0]].title)
 
  # Get requests
  print(datetime.datetime.now(), "[LOAD] requests")#, end=', ')
  requests = get_requests() 

  for test in test_list : 
    # print(test, type(args.test), "==", type(test.title), "->", args.test==test.title)

    if(not args.test or args.test==test.title) : 
      delete_directory_contents('index/')

      # vectorizer = Vectorizer(test.weight_schemat)
      print(datetime.datetime.now(), "[STARTING]", test.title.capitalize())

      # Tokenize docs
      print(datetime.datetime.now(), "[TOKENIZE]")
      preprocess_documents=tokenize(documents_metadata, test.pretreatment_type)  

      # Vectorize docs
      print(datetime.datetime.now(), "[INDEXING]")
      # documents_vectors=vectorizer.vectorize([doc.get('token') for doc in preprocess_documents]) # store vectors into database ? 
      indexing(preprocess_documents)

      # Tokenize requests, take in count the topic length (long our short)
      print(datetime.datetime.now(), "[BUILD] requests")
      build_request(test, requests)       
      
      preprocess_requests=tokenize_no_mp(requests, test.pretreatment_type) # print(preprocess_requests)
      # requests_vectors=vectorizer.vectorize([doc.get('token') for doc in preprocess_requests])

      # Search 
      print(datetime.datetime.now(), "[SEARCH]") 
      results=search(preprocess_requests, test) # Some are empty because request throw en exception 
      treq_run_paths = []
      for index,result in enumerate(results, start=1) : 
        trec_run_path = "TREC AP 88-90/TREC AP 88-90/trec_run/" + test.title + "_req_" + str(index) + ".txt"
        treq_run_paths.append(trec_run_path)
        write_run_file(result, trec_run_path)

      # Eval
      print(datetime.datetime.now(), "[EVAL]")    
      qrel_paths = "TREC AP 88-90/TREC AP 88-90/jugements de pertinence/qrels.1-50.AP8890.txt" #glob.glob('TREC AP 88-90/TREC AP 88-90/jugements de pertinence/*') 
      # TODO add time to process, number of documents in dataset.
      overall_result = trec_eval(qrel_paths, treq_run_paths)

      result_formated=format_res(overall_result)
     
      write_result({"result_formated" : result_formated,"overall_result" : overall_result},"results/" + test.title + ".txt")
      
if  __name__ == "__main__" : 
    run()
