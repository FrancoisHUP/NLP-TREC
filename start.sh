#!/bin/bash

# Define your list of arguments
args=(
    # "base_tfidf_short"
    # "base_tfidf_long"
    # "base_LMJelinekMercerSimilarity_short"
    # "base_LMJelinekMercerSimilarity_long"
    # "base_BM25_short"
    # "base_BM25_long" 
    # "lem_tfidf_short" 
    # "lem_tfidf_long" 
    # "lem_LMJM_short" 
    "lem_LMJM_long" 
    "lem_BM25_short"
    "lem_BM25_long"
    "steam_tfidf_short"
    "steam_tfidf_long"
    "steam_LMJM_short"
    "steam_LMJM_long"
    "steam_BM25_short" 
    "steam_BM25_long")

# Loop through each argument and call the Python script
for arg in "${args[@]}"
do
   python3 src/main.py -t $arg
done
