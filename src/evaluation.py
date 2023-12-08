

import pandas as pd
from trectools import TrecEval, TrecQrel, TrecRun
import tempfile
from collections.abc import Iterable
import glob

# def trec_eval(qrel_paths, trec_run_path):

#   # Create TrecRun object
#   run = TrecRun(trec_run_path) # Do run file for each single request 

#   qrel = TrecQrel("TREC AP 88-90/TREC AP 88-90/jugements de pertinence/qrels.1-50.AP8890.txt")

#   # Perform the evaluation
#   te = TrecEval(run, qrel)
  
#   # Calculate metrics
#   result = {}
#   result["num_ret"] = te.get_retrieved_documents(per_query=False)
#   result["num_rel"] = te.get_relevant_documents(per_query=False)
#   result["num_rel_ret"] = te.get_relevant_retrieved_documents(per_query=False)
#   result["num_q"] = len(te.run.topics())
#   result["map"] = calculate_map(te)
#   # result["map"] = te.get_map(depth=1000, per_query=True, trec_eval=True) # Dont work dont know why ?!
#   for v in [5, 10, 15, 20, 30, 100, 200, 500, 1000]:
#     result[f"P@{v}"] = te.get_precision(depth=v, per_query=False, trec_eval=True)

#   return result

from collections import defaultdict

def trec_eval(qrel_path, trec_run_paths):
    qrels= TrecQrel(qrel_path) # peut pas tout lire d'une shot yen a 50
    # Evaluate each query separately
    overall_result = {}
    for query_id in qrels.topics():
        qrel_paths = glob.glob('TREC AP 88-90/TREC AP 88-90/trec_qrels/*') 
        try : 
          run = TrecRun(trec_run_paths[int(query_id)-1])
          qrel= TrecQrel(qrel_paths[int(query_id)-1])
        except Exception :
            print("Error while evaluating ",int(query_id)-1," query" )
            continue
        te = TrecEval(run, qrel)

        result = {}
        result["num_ret"] = te.get_retrieved_documents(per_query=False)
        result["num_rel"] = te.get_relevant_documents(per_query=False)
        result["num_rel_ret"] = te.get_relevant_retrieved_documents(per_query=False)
        result["map"] = te.get_map(depth=1000, per_query=False, trec_eval=True) 
        # result["map_mine"] = calculate_map(te)
        for v in [5, 10, 15, 20, 30, 100, 200, 500, 1000]:
            result[f"P@{v}"] = te.get_precision(depth=v, per_query=False, trec_eval=True)

        overall_result[query_id] = result

    return overall_result

def calculate_map(te):
    relevan_documents = te.qrels.qrels_data
    retrieve_documents = te.run.run_data
    total_ap = 0
    num_queries = len(te.run.topics())

    for query_id in te.run.topics(): # should only be executed once 
        query_retrieved_docs = list(set(retrieve_documents.loc[retrieve_documents['query'] == query_id]['docid']))
        query_relevant_docs = relevan_documents.loc[relevan_documents['query'] == query_id]['docid']

        num_relevant_retrieved = 0
        sum_precision = 0

        for rank, doc_id in enumerate(query_retrieved_docs, start=1):
            if doc_id in query_relevant_docs.values:
                num_relevant_retrieved += 1
                precision_at_rank = num_relevant_retrieved / rank
                sum_precision += precision_at_rank

        ap = sum_precision / len(query_relevant_docs) if len(query_relevant_docs) > 0 else 0
        return ap
        # total_ap += ap

    # map_score = total_ap / num_queries
    # return map_score


# def eval(results,judgements):
#   avg_precision, avg_recall = calculate_precision_recall(results, judgements)
#   # calculate the MAP for each requests
#   for id,result in results.items() : 
#     true_judgments = [judgement['doc_id'] for judgement in judgements[id] if judgement['is_related']==True]
#     map_score = calculate_map(result,true_judgments)
#   return (avg_precision, avg_recall, map_score)

# def calculate_precision_recall(results, judgements):
#     # metrics = {}
#     precisions = []
#     recalls = []

#     for judgement_id, judgement_docs in judgements.items():
#         if judgement_id in results:
#             relevant_docs = results[judgement_id]

#             # Create a set of relevant document IDs for efficient lookup
#             relevant_docs_set = set(relevant_docs)

#             # Count the documents that are both in relevant_docs and have is_related True
#             relevant_retrieved = sum(doc['is_related'] and doc['doc_id'] in relevant_docs_set for doc in judgement_docs)

#             # Number of documents retrieved for this judgement_id
#             retrieved_docs_count = len(results[judgement_id])

#             # Calculate precision and recall
#             precision = relevant_retrieved / retrieved_docs_count if retrieved_docs_count else 0
#             precisions.append(precision)
           
#             recall = relevant_retrieved / sum(doc['is_related'] for doc in judgement_docs) if relevant_docs else 0
#             recalls.append(recall)

#             # metrics[judgement_id] = {"precision": precision, "recall": recall}

#     avg_precision = sum(precisions) / len(precisions)
#     avg_recall = sum(recalls) / len(recalls)
#     return avg_precision, avg_recall


# def calculate_map(results, relevant_documents):
#     """
#     Calculate the Mean Average Precision (MAP) given a list of relevant documents
#     and a list of retrieved documents (results).

#     :param relevant_documents: A list containing the relevant documents.
#     :param results: A list containing the retrieved documents in order of relevance.
#     :return: The MAP value.
#     """

#     # Store the precision values at each relevant document's rank
#     precisions = []

#     # Number of relevant documents found so far
#     relevant_found = 0

#     # Iterate through the results list
#     for k, doc in enumerate(results, start=1):
#         if doc in relevant_documents:
#             relevant_found += 1
#             precision_at_k = relevant_found / k
#             precisions.append(precision_at_k)

#     # Calculate MAP
#     map_value = sum(precisions) / len(relevant_documents) if relevant_documents else 0
#     return map_value

# # Example usage
# relevant_documents = ['doc' + str(i) for i in range(1, 101)]  # 100 relevant documents
# results = ['doc' + str(i) for i in range(1, 1001)]  # 1000 retrieved documents in order

# map_score = calculate_map(relevant_documents, results)
# map_score