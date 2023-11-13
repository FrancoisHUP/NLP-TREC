import gzip
import re
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

def tokenize(documents_metadata, pretreatment_type):
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    preprocess_documents = []

    for doc_id, data in documents_metadata.items():
        if "tokens" not in data:
            data["tokens"] = word_tokenize(data["text"].lower())

        if pretreatment_type == "basic":
            if "basic_token" not in data:
                data['basic_token'] = ' '.join(data["tokens"])
            preprocess_documents.append({"token":data['basic_token'],"doc_id":doc_id})

        elif pretreatment_type == "lemmatization":
            if "lemme_token" not in data:
                lemme_token = [lemmatizer.lemmatize(token) for token in data["tokens"] if token not in stop_words]
                data['lemme_token'] = ' '.join(lemme_token)
            preprocess_documents.append(data['lemme_token'])

        elif pretreatment_type == "stemming":
            if "stemme_token" not in data:
                stemme_token = [stemmer.stem(token) for token in data["tokens"] if token not in stop_words]
                data['stemme_token'] = ' '.join(stemme_token)
            preprocess_documents.append(data['stemme_token'])

        else:
            raise ValueError("Unknown tokenisation method")

    return preprocess_documents
        