
def eval(results,judgements):
  metrics = calculate_precision_recall(results, judgements)
  map_score = calculate_map(results, judgements)
  return (metrics,map_score)

def calculate_precision_recall(results, judgements):
  metrics = {}
  for index in judgements:
      judgement_docs = judgements[index]
      relevant_docs = results[int(index)]

      # Create a set of relevant document IDs for efficient lookup
      relevant_docs_set = set(relevant_docs)

      # Count the documents that are both in relevant_docs and have is_related True
      relevant_retrieved = sum(doc['is_related'] and doc['doc_id'] in relevant_docs_set for doc in judgement_docs)

      # relevant_retrieved = sum(doc_id in relevant_docs for doc_id in judgement_docs)

      precision = relevant_retrieved / len(judgement_docs) if judgement_docs else 0
      recall = relevant_retrieved / len(relevant_docs) if relevant_docs else 0

      metrics[index] = {"precision": precision, "recall": recall}
  return metrics

def calculate_map(results, judgements):
    average_precisions = []
    for request_id, retrieved_docs in judgements.items():
        relevant_docs = results.get(int(request_id))
        cum_relevant = 0
        precision_sum = 0
        for i, doc_id in enumerate(retrieved_docs, 1):
            if doc_id in relevant_docs:
                cum_relevant += 1
                precision_sum += cum_relevant / i
        average_precision = precision_sum / len(relevant_docs) if relevant_docs else 0
        average_precisions.append(average_precision)
    return sum(average_precisions) / len(average_precisions) if average_precisions else 0
