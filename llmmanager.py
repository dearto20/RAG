__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import httpx
from pathlib import Path
import tomli
import numpy as np
import chromadb

config = tomli.loads(Path('config.toml').read_text())
database = None
openai_client = httpx.Client(headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + config['openai_token']})

def get_embedding(text):
    response = openai_client.post('https://api.openai.com/v1/embeddings', 
        json = {'input': text, 'model': 'text-embedding-3-small', 'encoding_format': 'float'})
    embedding = response.json()['data'][0]['embedding']
    return embedding
    #return response.json()

def get_distance(vector_a, vector_b):
    return np.sum((np.asarray(vector_a) - np.asarray(vector_b)) ** 2)

def get_completions(text):
    response = openai_client.post('https://api.openai.com/v1/chat/completions', 
        json = {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': text}]})
    try:
        return response.json()['choices'][0]['message']['content']
        #return response.json()
    except:
        print('error in getting completions: ', response.json)
        raise

def get_database():
    global database
    if database is None:
        database = chromadb.PersistentClient(path='data')
    return database
