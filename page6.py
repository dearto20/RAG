from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore

import streamlit as st
import llmmanager
import pandas as pd

db = llmmanager.get_database()

def app():
    st.title('Ask LLM with Personal Context')

    query = st.text_input('Query')
    if query:
        print('Query: ', query)
    else:
        return
    
    st.write('Query is ' + query)
    
    collection = db.get_or_create_collection('context')
    vector_store = ChromaVectorStore(chroma_collection = collection)
    storage_context = StorageContext.from_defaults(vector_store = vector_store)
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context = storage_context
    )

    query_engine = index.as_query_engine()
    answer = query_engine.query(query)

    st.write(answer)
