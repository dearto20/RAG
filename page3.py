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
    st.write('Add New Embeddings into the DB (Edit the Default Text Shown Below)')

    text = 'I work in Samsung Electronics in Suwon-Si as a software developer, and commuting from Paygyo in Seongnam-si. I enjoy visualizing thoughts into programming code and see them work as expected. Sometimes, I play basketball early in the morning on weekends listening to music alone.'
    context = st.text_area('Sentences', value = text, height = 196)
    source = st.selectbox('Source', ('KG', 'Runestone', 'Etc'))
    chunk_size = int(st.radio("Chunk Size", ['256', '512', '1024']))

    if st.button('Save Embeddings'):
        collection = db.get_or_create_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_collection = collection)
        storage_context = StorageContext.from_defaults(vector_store = vector_store)
        doc = Document(text=context)
        documents = [doc]
        index = VectorStoreIndex.from_documents(
            documents, storage_context = storage_context,
            transformations = [SentenceSplitter(chunk_size=chunk_size)]
        )

        st.toast('Save Finished')