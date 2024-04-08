import streamlit as st
import llmmanager
import uuid
import re

def app():
    db = llmmanager.get_database()

    st.title('Personal Context Management')
    
    st.divider()
    st.write('Remove All Sentences from the DB')
    if st.button("Reset Database"):
        try:
            db.delete_collection('context')
        except ValueError:
            pass
        st.toast('Reset Finished')
    
    st.divider()
    context = st.text_area('Sentence')
    source = st.selectbox('Source', ('Runestone', 'Etc'))
    chunk_size = int(st.radio("Chunk Size", ["16", "32", "64"]))

    if st.button("Push Into RAG DB"):
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

            if chunk_size > 0:
                words = re.findall(r'\S+', sentence)
                index = 0
                while cur_words := words[index:index + chunk_size]:
                    index += chunk_size // 2
                    chunk = ' '.join(cur_words)
                    st.write(f'Chunk: {chunk}')
                    add_chunk(chunk, sentence) 
