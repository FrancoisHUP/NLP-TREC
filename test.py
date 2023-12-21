from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key= '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' # os.environ.get("OPENAI_API_KEY"),
)

query = 'diabetes type 2 effect on organ tissues'

# Define the prompt you want to send
prompt = '''
    Expand the following search query for a more comprehensive search in a medical database. Original query: 
    'type 2 diabetes'. Include synonyms, related conditions, and treatment options. Avoid overly technical 
    terms and provide the expanded query terms in a list format.
''' + query


completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)

# Print the response
print(completion.choices[0].message.content)
print('prompt : ', prompt)