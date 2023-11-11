class Test:
  def __init__(self,title,pretreatment_type, weight_schemat, request_lenght):
    self.title = title
    self.pretreatment_type = pretreatment_type
    self.weight_schemat = weight_schemat
    self.request_lenght = request_lenght

  def __repr__(self):
    return self.title
  

test_list = [ 
  # Base test
  Test("base_nf_short", "basic", "normalized_frequency", "short"),
  Test("base_nf_long", "basic", "normalized_frequency", "long"),
  Test("base_tfidf_short", "basic", "tf_idf_normalize", "short"),
  Test("base_tfidf_long", "basic", "tf_idf_normalize", "long"),
  Test("base_BM25_short", "basic", "BM25", "short"),
  Test("base_BM25_long", "basic", "BM25", "long"),
  # Lemmatization
  Test("lem_nf_short", "lemmatization", "normalized_frequency", "short"),
  Test("lem_nf_long", "lemmatization", "normalized_frequency", "long"),
  Test("lem_nf_short", "lemmatization", "tf_idf_normalize", "short"),
  Test("lem_nf_long", "lemmatization", "tf_idf_normalize", "long"),
  Test("lem_BM25_short", "lemmatization", "BM25", "short"),
  Test("lem_BM25_long", "lemmatization", "BM25", "long"),
  # Steaming
  Test("steam_nf_short", "stemming", "normalized_frequency", "short"),
  Test("steam_nf_long", "stemming", "normalized_frequency", "long"),
  Test("steam_nf_short", "stemming", "tf_idf_normalize", "short"),
  Test("steam_nf_long", "stemming", "tf_idf_normalize", "long"),
  Test("steam_BM25_short", "stemming", "BM25", "short"),
  Test("steam_BM25_long", "stemming", "BM25", "long"),
  ]