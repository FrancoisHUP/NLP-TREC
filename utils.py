import glob
import gzip
import re

doc_pattern = re.compile(r'<DOC>(.*?)</DOC>', re.DOTALL)
docno_pattern = re.compile(r'<DOCNO>\s*(.*?)\s*</DOCNO>')
head_pattern = re.compile(r'<HEAD>\s*(.*?)\s*</HEAD>')
text_pattern = re.compile(r'<TEXT>\s*(.*?)\s*</TEXT>', re.DOTALL)

def get_documents() :
    """
    return a dictionary of documents with key = doc_id and value = {'title': title, 'text': text}. 
    output example :
        documents["AP880212-0001"] = 
        {'title': 'Reports Former Saigon Officials Released from Re-education Camp', 
        'text': "More than 150 former officers of the\noverthrown ..."}
    """
    documents_metadata = {}
    # Get a list of all .gz files in the "Ap" directory
    file_list = glob.glob('TREC AP 88-90/TREC AP 88-90/collection de documents/AP/*.gz') # start from ../src

    # Loop over the list of files
    for filename in file_list:
        
        # Open the .gz file
        with gzip.open(filename, 'rt', encoding='latin1') as file:  # 'rt' mode for text reading
            # Read the contents of the file
            content = file.read()
            for doc in doc_pattern.finditer(content):
                doc_content = doc.group(1)

                # Extracting individual elements
                doc_id = docno_pattern.search(doc_content).group(1)
                head = head_pattern.search(doc_content)
                text = text_pattern.search(doc_content)
                
                documents_metadata[doc_id] = {
                    'title': head.group(1) if head else 'Default Title',
                    'text': text.group(1) if text else 'Default text'
                }  

    return documents_metadata

documents = get_documents()
print(documents["AP880212-0001"]) 

import glob
import gzip
import re

topic_pattern = re.compile(r'<top>(.*?)</top>', re.DOTALL)
# Regular expressions for individual elements
num_pattern = re.compile(r'<num>\s*Number:\s*(\d+)')
title_pattern = re.compile(r'<title>\s*Topic:\s*(.*?)\s*\n')
desc_pattern = re.compile(r'<desc>\s*Description:\s*(.*?)\s*<narr>', re.DOTALL)

def get_requests() :
    """
    return a dictionary of requests with key = request_id and value = {'title': title, 'desc': desc}.
    output example :
        requests["001"] = {'title': 'Antitrust Cases Pending', 'desc': 'Document discusses a pending antitrust case.'}
    """
    requests_metadata = {}
    
    # Get a list of all topics files in the "Topics-requetes" directory
    file_list = glob.glob('TREC AP 88-90/TREC AP 88-90/Topics-requetes/*') 
    # Loop over the list of files
    for filename in file_list:

        # Open the .gz file
        with open(filename, 'r') as file:
            # Read the content of the file
            topic_requests_string = file.read()
            for topic in topic_pattern.finditer(topic_requests_string):
                topic_content = topic.group(1)

                # Extracting individual elements
                num = num_pattern.search(topic_content)
                title = title_pattern.search(topic_content)
                desc = desc_pattern.search(topic_content)
                
                if(num) :
                    requests_metadata[num.group(1)] = {
                        'title': title.group(1) if title else None,
                        'desc': desc.group(1).strip() if desc else None
                    }
        
    return requests_metadata 
requests = get_requests() 
print("Total number of request : ", len(requests))
print(requests["001"])

def build_request(req_lenght, requests) :
  built_requests = {}
  for request_id,request_data in requests.items() :  
    request_string = request_data['title']
    if req_lenght=="long" : 
      request_string += " " + request_data['desc']
    built_requests[request_id] = request_string
  return built_requests
    
# Build requests 
short_requests = build_request('short', requests)       
long_requests = build_request('long', requests)   
print("Short request : ", short_requests["001"])    
print("Long request : ", long_requests["001"])    

import java
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.analysis.core import StopFilter
from org.apache.lucene.analysis import CharArraySet
from org.apache.lucene.analysis.en import PorterStemFilter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()

def lemmatize(text):
    words = word_tokenize(text)
    lemmas = [lemmatizer.lemmatize(word, pos=wordnet.VERB) for word in words]
    return lemmas #' '.join(lemmas)

def tokenize(text, preprocess_method):
    tokens = []
    if preprocess_method == "lemmatization":
        tokens = lemmatize(text)
    else : 
        analyzer = StandardAnalyzer()
        stream = analyzer.tokenStream(None, text)
        # Stemming 
        if preprocess_method == "stemming":
            stream = PorterStemFilter(stream)

        # Stop words
        stop_words_list = java.util.ArrayList()
        for word in nltk_stop_words: #["and", "is", "the", "this"]
            stop_words_list.add(word)
        stop_words = CharArraySet(stop_words_list, True)
        stream = StopFilter(stream, stop_words)

        term = stream.getAttribute(CharTermAttribute.class_)
        stream.reset()

        while stream.incrementToken():
            tokens.append(term.toString())
        stream.end()
        analyzer.close()

    return tokens

# Example of tokenization
test_document = "This is a sample document."
tokens = tokenize(test_document, "stemming")
print(tokens)