import gzip
import re
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

class Tokenizer() :
    """
    Preprocess text : [basic,  stemmer or lemmatizer (last two including stop words)] 
    """    
    def __init__(self, 
        stop_words=set(stopwords.words('english')), 
        stemmer=PorterStemmer(), 
        lemmatizer=WordNetLemmatizer()):

        self.stop_words=stop_words
        self.stemmer=stemmer
        self.lemmatizer=lemmatizer

        
        self.inverted_index_basic=defaultdict(set)
        self.inverted_index_lemma=defaultdict(set)
        self.inverted_index_stemme=defaultdict(set)
    
    def tokenize(self, documents_metadata, pretreatment_type) :
        if(pretreatment_type == "basic") : 
            self.tokenize_basic(documents_metadata)
            return self.inverted_index_basic
        if(pretreatment_type == "lemmatization") : 
            self.tokenize_lemmatizer(documents_metadata)
            return self.inverted_index_lemma
        if(pretreatment_type == "stemmer") : 
            self.tokenize_stemmer(documents_metadata)
            return self.inverted_index_stemme

    def tokenize_basic(self, documents_metadata):
        # Tokenize the text into words
        if(not self.inverted_index_basic) :
            for doc_id, data in documents_metadata.items():
                tokens = word_tokenize(data["text"].lower())
                # for token in tokens:
                #     if token not in self.stop_words:
                #         self.inverted_index_basic[token].add(doc_id)
 
    def tokenize_lemmatizer(self, documents_metadata):
        if(not self.token_lemmatize) :
            for doc_id, data in documents_metadata.items():
                tokens = word_tokenize(data["text"].lower())
                # for token in tokens:
                #     if token not in self.stop_words:
                #         lemma_token = lemmatizer.lemmatize(token)
                #         inverted_index[lemma_token].add(doc_id)
    
    def tokenize_stemmer(self, documents_metadata):
        if(not self.token_stemme) :
            for doc_id, data in documents_metadata.items():
                tokens = word_tokenize(data["text"].lower())
                # for token in tokens:
                #     if token not in self.stop_words:
                #         stemmed_token = stemmer.stem(token)
                #         self.inverted_index_basic[stemmed_token].add(doc_id)

# self.token_stemme=[self.stemmer.stem(word) for word in words if word not in stop_words and word.isalpha()]
