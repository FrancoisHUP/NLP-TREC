from sklearn.feature_extraction.text import TfidfVectorizer


class Vectorizer() :
    """
    Vectorize document from tokens
    """    
    def __init__(self, vectorizer) : 
        self.vectorizer=TfidfVectorizer()

    def vectorize(tokens) : 
        tfidf_matrix = vectorizer.fit_transform(documents)
        return tfidf_matrix