import argparse
import nltk
import nltk.data
from test import test_list
import sys

def check_cli_args() : 
  args = parse_cli()
  check_args(args)
  return args

def parse_cli() :
  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--no-download", action="store_true", help="Specify this flag to disable downloading.")
  parser.add_argument("-l", "--list", action="store_true", help="List all the availaible test")
  parser.add_argument("-t", "--test", type=str, help="Specify the test to run")
  # TODO add arg to skip the indexation and run the tests with existing index
  return parser.parse_args()

def check_args(args) : 
  if(args.list) : 
    print("Tests List:")
    for test in test_list : 
      print(test.title)
    sys.exit("Error message")

  if(not args.no_download) : 
    downloads()
    
  if(args.test) :
    print("[RUN ",  args.test, "]")
  else: 
    print("[RUN : ALL]")

def downloads():
    # print("[DOWNLOADS]")
    # Dictionary of packages and their corresponding paths in NLTK data
    packages = {
        'punkt': 'tokenizers/punkt',
        'stopwords': 'corpora/stopwords.zip',
        'wordnet': 'corpora/wordnet.zip',
        'omw-1.4': 'corpora/omw-1.4.zip'
    }

    for package, path in packages.items():
        try:
            # Check if the package is already installed
            nltk.data.find(path)
            # print(f"'{package}' is already installed.")
        except LookupError:
            # If not installed, download the package
            nltk.download(package)


  