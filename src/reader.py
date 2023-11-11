import glob
import gzip
import re
import xml.etree.ElementTree as ET

def xml_to_pyobject(xml_data) :
    print(xml_data)
    try :
        root = ET.fromstring(xml_data) 
        doc_data = {}
        for child in root:
            doc_data[child.tag] = child.text.strip() if child.text else None
        return doc_data
    except Exception as e:
       # By this way we can know about the type of error occurring
        print("The error is: ",e)

def extract_doc_data(doc) :
    doc_data = {}
    # Use regular expressions to extract the content of the <DOCNO> tag
    match = re.search(r'<DOCNO>(.*?)</DOCNO>', doc, re.DOTALL)
    if match:
        doc_data["DOCNO"] = match.group(1).strip()
        
    match = re.search(r'<TEXT>(.*?)</TEXT>', doc, re.DOTALL)
    if match:
        doc_data["TEXT"] = match.group(1).strip()

    match = re.search(r'<HEAD>(.*?)</HEAD>', doc, re.DOTALL)
    if match:
        doc_data["HEAD"] = match.group(1).strip()
    return doc_data

def extract_DOCNO_from_doc(doc):
    # Use regular expressions to extract the content of the <DOCNO> tag
    match = re.search(r'<DOCNO>(.*?)</DOCNO>', doc, re.DOTALL)
    if match:
        return match.group(1).strip()  # Return the text content without the <TEXT> tags
    return ""

# Function to extract individual documents from the file content
def extract_documents(text):
    # Split the text into documents using the <DOC> tag
    documents = re.split(r'</DOC>', text)
    # Remove the first and last elements which are not actual documents
    if documents:
        documents = documents[:-1]
    return [doc + '</DOC>' for doc in documents] 

def get_documents() :
    documents=[]
    
    # Get a list of all .gz files in the "Ap" directory
    # file_list = glob.glob('../TREC AP 88-90/TREC AP 88-90/collection de documents/AP/*.gz') # start from src 
    file_list = glob.glob('TREC AP 88-90/TREC AP 88-90/collection de documents/AP/*.gz') # start from 
    # Loop over the list of files
    for filename in file_list:
        
        # Open the .gz file
        with gzip.open(filename, 'rt') as file:  # 'rt' mode for text reading
            # Read the contents of the file
            content = file.read()
            documents = extract_documents(content)

    documents_metadata = {}

    for doc in documents:
        doc_data = extract_doc_data(doc)
        doc_id = doc_data["DOCNO"] # Extract the document ID
        
        # Store document metadata
        documents_metadata[doc_id] = {
            'title': doc_data.get('HEAD', 'Default Title'),  # Provide a default title if 'HEAD' is not present
            'text' : doc_data.get('TEXT', '')  # Provide an empty string if 'TEXT' is not present
        }
    return documents_metadata 
            


