import llmmanager
from llama_index.core import Document
from llama_index.core import Settings
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from pathlib import Path

import streamlit as st
import tomli
import os
import re
import uuid

def app():
    config = tomli.loads(Path('config.toml').read_text())
    os.environ['OPENAI_API_KEY'] = config['openai_token']
    Settings.embed_model = OpenAIEmbedding()

    db = llmmanager.get_database()
    collection_name = 'context_with_llamaindex'

    st.title('Manage Personal Context in the Local DB')
    
    st.write('Remove All Embeddings in the DB')
    if st.button('Reset Database'):
        try:
            db.delete_collection(collection_name)
        except ValueError:
            pass
        st.toast('Reset Finished')
    
    st.divider()
    st.write('Add New Embeddings into the DB')

    context = st.text_area('Sentences', height = 196)
    source = st.selectbox('Source', ('KG', 'Runestone', 'Etc'))
    chunk_size = int(st.radio("Chunk Size", ['256', '512', '1024']))

    collection_name = 'context_with_llamaindex'
    collection = db.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection = collection)
    storage_context = StorageContext.from_defaults(vector_store = vector_store)
    doc = Document(text = context, metadata = {"sentence": context})
    documents = [doc]
    text_splitter = SentenceSplitter(chunk_size = chunk_size, chunk_overlap = 10)
    Settings.text_splitter = text_splitter    
        
    if st.button('Set Embeddings'):
        index = VectorStoreIndex.from_documents(
            documents, storage_context = storage_context,
            transformations = [text_splitter]
        )
        st.toast('Set Finished')
    if st.button('Add Embeddings'):
        index = VectorStoreIndex.from_vector_store(
            vector_store, storage_context = storage_context,
            transformations = [text_splitter]
        )
        index.insert(doc)
        st.toast('Add Finished')
