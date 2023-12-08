from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import multiprocessing

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

from concurrent.futures import ProcessPoolExecutor, as_completed

def tokenize(documents_metadata, pretreatment_type):
    preprocess_documents = []

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_document, data, pretreatment_type, doc_id) 
                   for doc_id, data in documents_metadata.items()]

        for future in as_completed(futures):
            try:
                result = future.result()
                preprocess_documents.append(result)
            except Exception as e:
                print(f"A process encountered an exception: {e}")

    return preprocess_documents


# def tokenize(documents_metadata, pretreatment_type):
#     preprocess_documents = []

#     # Setting up the process pool
#     with multiprocessing.Pool() as pool:
#         # Map each document to a process in the pool
#         results = pool.starmap(
#             process_document, 
#             [(data, pretreatment_type, doc_id) for doc_id, data  in documents_metadata.items()]
#         )
#         preprocess_documents.extend(results)

#     return preprocess_documents

def tokenize_no_mp(documents_metadata, pretreatment_type):
    preprocess_documents = []
    for doc_id, data  in documents_metadata.items() : 
        preprocess_documents.append(process_document(data, pretreatment_type, doc_id))
    return preprocess_documents

def process_document(data, pretreatment_type, doc_id):

    try:
        preprocess_documents = None
        
        # for doc_id, data in documents_metadata.items():
        if "tokens" not in data:
            data["tokens"] = word_tokenize(data["text"].lower())
            data['token_title'] = word_tokenize(data["title"].lower())

        if pretreatment_type == "basic":
            if "basic_token" not in data:
                data['basic_token'] = ' '.join(data["tokens"])
                data['basic_token_title'] = ' '.join(data["token_title"])
            preprocess_documents = {"token":data['basic_token'],"doc_id":doc_id,"title":data["basic_token_title"]}

        elif pretreatment_type == "lemmatization":
            if "lemme_token" not in data:
                lemme_token = [lemmatizer.lemmatize(token) for token in data["tokens"] if token not in stop_words]
                data['lemme_token'] = ' '.join(lemme_token)
                lemme_token_title = [lemmatizer.lemmatize(token) for token in data["token_title"] if token not in stop_words]
                data['lemme_token_title'] = ' '.join(lemme_token_title)
            preprocess_documents =  {"token":data['lemme_token'],"doc_id":doc_id,"title":data["lemme_token_title"]} 

        elif pretreatment_type == "stemming":
            if "stemme_token" not in data:
                stemme_token = [stemmer.stem(token) for token in data["tokens"] if token not in stop_words]
                data['stemme_token'] = ' '.join(stemme_token)
                stemme_token_title = [stemmer.stem(token) for token in data["token_title"] if token not in stop_words]
                data['stemme_token_title'] = ' '.join(stemme_token_title)
            preprocess_documents = {"token":data['stemme_token'],"doc_id":doc_id,"title":data["stemme_token_title"]}

        else:
            raise ValueError("Unknown tokenisation method")
    
        return preprocess_documents
    
    except Exception as e:
        # Log the exception (consider using a logging library here)
        print(f"Error processing document {doc_id}: {e}")

        # Return error information (could be a simple flag or detailed error message)
        return {"error": True, "message": str(e), "doc_id": doc_id}
