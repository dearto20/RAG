import streamlit as st
import llmmanager
import uuid
import re

CHUNK_SIZE = 10

def app():
    db = llmmanager.get_database()

    st.title('Add Contexts Into RAG DB')

    st.write('Remove All Contexts in the DB')
    if st.button("Reset Database"):
        try:
            db.delete_collection('context')
        except ValueError:
            pass
        st.toast('Reset Finished')

    context = st.text_area('Sentence')
    source = st.selectbox('Source', ('Runestone', 'Etc'))
    use_chunk = st.checkbox('Split into Chunks')

    if st.button("Push Contexts"):
        collection = db.get_or_create_collection('context')
        def add_chunk(chunk, sentence):
            embedding = llmmanager.get_embedding(chunk)
            collection.add(ids=[str(uuid.uuid4())], embeddings=[embedding], metadatas=[{'chunk': chunk, 'sentence': sentence, 'source': source}])

        for sentence in re.split(r'\.|\n\n', context):
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
