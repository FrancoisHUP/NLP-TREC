

import lucene
from java.io import File
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.similarities import ClassicSimilarity, BM25Similarity, LMJelinekMercerSimilarity, BooleanSimilarity

from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.store import MMapDirectory, FSDirectory
from org.apache.lucene.document import Document, Field, FieldType

from org.apache.lucene.queryparser.classic import QueryParser

import re

# import multiprocessing
# from multiprocessing import Pool
# from functools import partial

from  test import Test 

# Initialize Lucene and the JVM
lucene.initVM()
# print(lucene.VERSION)

# Create an on-disk index using MMapDirectory
index_path = Paths.get("index")  # Specify your index path here

### INDEXING ### 
def add_doc(w, doc_id, title, content):
    t1 = FieldType()
    t1.setStored(True)
    t1.setTokenized(False)
    t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

    t2 = FieldType()
    t2.setStored(False)
    t2.setTokenized(True)
    t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    doc = Document()
    doc.add(Field("doc_id", doc_id, t1))
    doc.add(Field("title", title, t1))
    doc.add(Field("contents", content, t2))
    w.addDocument(doc)

def indexing(preprocess_documents) :
    index = MMapDirectory(index_path)
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    writer = IndexWriter(index, config)

    for preprocess_document in preprocess_documents: 
        # Add some documents
        add_doc(writer, preprocess_document["doc_id"], preprocess_document["title"], preprocess_document["token"])
    # Commit and close the writer
    writer.close()

### SEARCHING ### 
def set_similirity_weight_schemat(searcher, weight_schemat) :
    if weight_schemat == Test.ClassicSimilarity : 
        searcher.setSimilarity(ClassicSimilarity())
    if weight_schemat == Test.BM25Similarity : 
        searcher.setSimilarity(BM25Similarity(1.2,0.75))
    if weight_schemat == Test.LMJelinekMercerSimilarity : 
        searcher.setSimilarity(LMJelinekMercerSimilarity(0.7))
    if weight_schemat == Test.BooleanSimilarity : 
        searcher.setSimilarity(BooleanSimilarity())

def search(preprocess_requests, test: Test):
    results=[]
    directory = FSDirectory.open(File("index/").toPath())
    analyzer = StandardAnalyzer()
    searcher = IndexSearcher(DirectoryReader.open(directory))
    set_similirity_weight_schemat(searcher, test.weight_schemat)

    for index,preprocess_request in enumerate(preprocess_requests):
        result = []
        if index > 49 : 
            break
        query_string = preprocess_request["token"].replace("/", "").replace("?", "").replace("`", "").replace("(", "").replace(")", "")
        query_id = preprocess_request["doc_id"]
        try :
            query = QueryParser("contents", analyzer).parse(query_string)
        except Exception:
            print("Error when parse '",query_string,"'" )
            continue
        scoreDocs = searcher.search(query, 1000).scoreDocs

        for rank, scoreDoc in enumerate(scoreDocs, start=1):
            doc = searcher.doc(scoreDoc.doc)
            doc_id = doc.get("doc_id")
            score = scoreDoc.score

            # Append results in TREC format: query_id, Q0, doc_id, rank, score, run_tag
            result.append((query_id, "Q0", doc_id, rank, score, test.title))
        
        results.append(result)

    return results


