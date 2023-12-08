import glob
import gzip
import re
# from loading import progressBar

doc_pattern = re.compile(r'<DOC>(.*?)</DOC>', re.DOTALL)
# Regular expressions for individual elements
docno_pattern = re.compile(r'<DOCNO>\s*(.*?)\s*</DOCNO>')
head_pattern = re.compile(r'<HEAD>\s*(.*?)\s*</HEAD>')
text_pattern = re.compile(r'<TEXT>\s*(.*?)\s*</TEXT>', re.DOTALL)

def get_documents() :
    documents_metadata = {}
    # Get a list of all .gz files in the "Ap" directory
    # file_list = glob.glob('../TREC AP 88-90/TREC AP 88-90/collection de documents/AP/*.gz') # start from src 
    file_list = glob.glob('TREC AP 88-90/TREC AP 88-90/collection de documents/AP/*.gz') # start from ../src

    # Loop over the list of files
    # for filename in progressBar(file_list, prefix = '[READ DOCS]', suffix = 'Complete', length = 50):
    for index,filename in enumerate(file_list):
        # if index>10 : 
            # break
        
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

topic_pattern = re.compile(r'<top>(.*?)</top>', re.DOTALL)
# Regular expressions for individual elements
num_pattern = re.compile(r'<num>\s*Number:\s*(\d+)')
title_pattern = re.compile(r'<title>\s*Topic:\s*(.*?)\s*\n')
desc_pattern = re.compile(r'<desc>\s*Description:\s*(.*?)\s*<narr>', re.DOTALL)

def get_requests() :
    requests_metadata = {}
    
    # Get a list of all topics files in the "Topics-requetes" directory
    file_list = glob.glob('TREC AP 88-90/TREC AP 88-90/Topics-requetes/*') 
    # Loop over the list of files
    # for filename in progressBar(file_list, prefix = '[READ REQS]', suffix = 'Complete', length = 50):
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

def get_judgement() :    
    # Get a list of all topics files in the "Topics-requetes" directory
    file_list = glob.glob('TREC AP 88-90/TREC AP 88-90/jugements de pertinence/*') 
    judgements_metadata = {}

    # Loop over the list of files
    # for filename in progressBar(file_list, prefix = '[READ JUDS]', suffix = 'Complete', length = 50):
    for filename in file_list:
        with open(filename, 'r') as file:
            for line in file:
                components = line.strip().split(' ')
                
                topic_id = components[0]
                document_id = components[2]
                is_related = components[3] == '1'

                # Initialize a list for the topic_id if it does not exist
                if int(topic_id) not in judgements_metadata:
                    judgements_metadata[int(topic_id)] = []

                # Append the object to the list for the topic_id
                new_object = {
                    'doc_id': document_id,
                    'is_related': is_related
                }
                judgements_metadata[int(topic_id)].append(new_object)  # Append new_object to the list

    return judgements_metadata


