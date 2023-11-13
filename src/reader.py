import glob
import gzip
import re
import xml.etree.ElementTree as ET

cap_number_of_read=10 # TODO rmv, for testing

doc_pattern = re.compile(r'<DOC>(.*?)</DOC>', re.DOTALL)
# Regular expressions for individual elements
docno_pattern = re.compile(r'<DOCNO>\s*(.*?)\s*</DOCNO>')
head_pattern = re.compile(r'<HEAD>\s*(.*?)\s*</HEAD>')
text_pattern = re.compile(r'<TEXT>\s*(.*?)\s*</TEXT>', re.DOTALL)

def get_documents() :
    documents=[]
    
    # Get a list of all .gz files in the "Ap" directory
    # file_list = glob.glob('../TREC AP 88-90/TREC AP 88-90/collection de documents/AP/*.gz') # start from src 
    file_list = glob.glob('TREC AP 88-90/TREC AP 88-90/collection de documents/AP/*.gz') # start from 

    # count = 0 # TODO rmv, for testing
    # Loop over the list of files
    for filename in file_list:
        # count += 1 # TODO rmv, for testing
        # if(count>cap_number_of_read): # TODO rmv at some point
            # break # TODO rmv at some point

        # Open the .gz file
        with gzip.open(filename, 'rt') as file:  # 'rt' mode for text reading
            # Read the contents of the file
            content = file.read()
            documents.append(content)
        
    documents_metadata = {}

    # Iterating over each matched DOC block
    for doc_string in documents:
        for doc in doc_pattern.finditer(doc_string):
            doc_content = doc.group(1)

            # Extracting individual elements
            doc_id = docno_pattern.search(doc_content).group(1)
            head = head_pattern.search(doc_content)
            text = text_pattern.search(doc_content)

            # Populating the dictionary
            documents_metadata[doc_id] = {
                'title': head.group(1) if head else 'Default Title',
                'text': text.group(1) if text else ''
            }

    return documents_metadata 

topic_pattern = re.compile(r'<top>(.*?)</top>', re.DOTALL)
# Regular expressions for individual elements
num_pattern = re.compile(r'<num>\s*Number:\s*(\d+)')
title_pattern = re.compile(r'<title>\s*Topic:\s*(.*?)\s*\n')
desc_pattern = re.compile(r'<desc>\s*Description:\s*(.*?)\s*<narr>', re.DOTALL)

def get_requests() :
    topic_requests=[]
    
    # Get a list of all topics files in the "Topics-requetes" directory
    file_list = glob.glob('TREC AP 88-90/TREC AP 88-90/Topics-requetes/*') 
    # Loop over the list of files
    for filename in file_list:

        # Open the .gz file
        with open(filename, 'r') as file:
            # Read the content of the file
            content = file.read()
            topic_requests.append(content)

    requests_metadata = {}

    # Iterating over each matched DOC block
    for topic_requests_string in topic_requests:
        for topic in topic_pattern.finditer(topic_requests_string):
            topic_content = topic.group(1)

            # Extracting individual elements
            num = num_pattern.search(topic_content)
            title = title_pattern.search(topic_content)
            desc = desc_pattern.search(topic_content)
            
          
            # Populating the dictionary
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
    for filename in file_list:

        # Open the .gz file
        with open(filename, 'r') as file:
            for line in file:
                # Split the line into components
                components = line.strip().split(' ')
                
                # Extract the relevant information
                topic_id = components[0]
                document_id = components[2]
                is_related = components[3] == '1'
                
                # Initialize a list for the topic_id if it does not exist
                if topic_id not in judgements_metadata:
                    judgements_metadata[topic_id] = []

                # Append the object to the list for the topic_id
                judgements_metadata[topic_id].append({
                    'doc_id': document_id,
                    'is_related': is_related
                })
    
    return judgements_metadata 
            


