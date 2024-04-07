import streamlit as st
import llmmanager
import uuid
import re

CHUNK_SIZE = 10

def app():
    db = llmmanager.get_database()

    st.title('Configure RAG')
    st.write('Put Contexts into Vector DB')

    if st.button("Init Database"):
        try:
            db.delete_collection('context')
        except ValueError:
            pass
        st.toast('Init Finished');

    ctx = st.text_area('Context')
    source = st.text_input('Source')
    use_chunk = st.checkbox('Split into Chunks')

    if st.button("Read Sentence"):
        collection = db.get_or_create_collection('context')
        def add_chunk(chunk, sentence):
            embedding = llmmanager.get_embedding(chunk)
            collection.add(ids=[str(uuid.uuid4())], embeddings=[embedding], metadatas=[{'chunk': chunk, 'sentence': sentence, 'source': source}])

        for sentence in re.split(r'\.|\n\n', ctx):
            sentence = re.sub(r'\s{2, }', ' ', sentence).strip()
            if not sentence:
                continue

            st.write(f'Sentence: {sentence}')
            add_chunk(sentence, sentence)

            if use_chunk:
                words = re.findall(r'\S+', sentence)
                index = 0
                while cur_words := words[index:index + CHUNK_SIZE]:
                    index += CHUNK_SIZE // 2
                    chunk = ' '.join(cur_words)
                    st.write(f'Chunk: {chunk}')
                    add_chunk(chunk, sentence) 
