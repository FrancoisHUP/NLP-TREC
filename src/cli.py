import argparse
import nltk
from test import test_list

def check_cli_args() : 
  args = parse_cli()
  check_args(args)
  return args

def parse_cli() :
  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--no-download", action="store_true", help="Specify this flag to disable downloading.")
  parser.add_argument("-l", "--list", action="store_true", help="List all the availaible test")
  parser.add_argument("-t", "--test", type=str, help="Specify the test to run")
  return parser.parse_args()

def check_args(args) : 
  if(args.list) : 
    print("Tests List:")
    for test in test_list : 
      print(test.title)
    return None 

  if(not args.no_download) : 
    downloads()
    
  if(args.test) :
    print("[RUN ",  args.test, "]")
  else: 
    print("[RUN : ALL TESTS]")

def downloads() : 
  # Download required NLTK data
  print("[DOWNLOAD]")
  nltk.download('punkt')
  nltk.download('stopwords')
  nltk.download('wordnet')
  nltk.download('omw-1.4')

  