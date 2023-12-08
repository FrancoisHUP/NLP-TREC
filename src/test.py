class Test:
  ClassicSimilarity="ClassicSimilarity"
  BM25Similarity="BM25Similarity"
  LMJelinekMercerSimilarity="LMJelinekMercerSimilarity"
  BooleanSimilarity="BooleanSimilarity"
  def __init__(self,title,pretreatment_type, weight_schemat, request_lenght):
    self.title = title
    self.pretreatment_type = pretreatment_type
    self.weight_schemat = weight_schemat
    self.request_lenght = request_lenght

  def __repr__(self):
    return self.title

test_list = [ 
  # Base test
  # Test("base_tfidf_short", "basic", "ClassicSimilarity", "short"),
  # Test("base_tfidf_long", "basic", "ClassicSimilarity", "long"),
  # Test("base_LMJelinekMercerSimilarity_short", "basic", "LMJelinekMercerSimilarity", "short"),
  # Test("base_LMJelinekMercerSimilarity_long", "basic", "LMJelinekMercerSimilarity", "long"),
  # Test("base_BM25_short", "basic", "BM25Similarity", "short"),
  # Test("base_BM25_long", "basic", "BM25Similarity", "long"),
  # # Lemmatization
  # Test("lem_tfidf_short", "lemmatization", "ClassicSimilarity", "short"),
  # Test("lem_tfidf_long", "lemmatization", "ClassicSimilarity", "long"),
  Test("lem_LMJM_short", "lemmatization", "LMJelinekMercerSimilarity", "short"),
  Test("lem_LMJM_long", "lemmatization", "LMJelinekMercerSimilarity", "long"),
  Test("lem_BM25_short", "lemmatization", "BM25Similarity", "short"),
  Test("lem_BM25_long", "lemmatization", "BM25Similarity", "long"),
  # Steaming
  Test("steam_tfidf_short", "stemming", "ClassicSimilarity", "short"),
  Test("steam_tfidf_long", "stemming", "ClassicSimilarity", "long"),
  Test("steam_LMJM_short", "stemming", "LMJelinekMercerSimilarity", "short"),
  Test("steam_LMJM_long", "stemming", "LMJelinekMercerSimilarity", "long"),
  Test("steam_BM25_short", "stemming", "BM25Similarity", "short"),
  Test("steam_BM25_long", "stemming", "BM25Similarity", "long"),

  # Other tests
  # Test("steam_Bool_short", "stemming", "BooleanSimilarity", "short"),
  # Test("steam_Bool_long", "stemming", "BooleanSimilarity", "long"),
  ]