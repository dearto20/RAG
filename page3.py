import streamlit as st
import llmmanager
import uuid
import re

def app():
    db = llmmanager.get_database()

    st.title('Manage Personal Context in DB')
    
    st.write('Remove All Embeddings in DB')
    if st.button("Reset Database"):
        try:
            db.delete_collection('context')
        except ValueError:
            pass
        st.toast('Reset Finished')
    
    st.divider()
    st.write('Add New Embeddings into DB')

    if 'context' not in st.session_state:
        st.session_state['context'] = ""

    context = st.text_area('Sentences', key = 'context', value = st.session_state.get('context', ''))
    source = st.selectbox('Source', ('KG', 'Runestone', 'Etc'))
    chunk_size = int(st.radio("Chunk Size", ["16", "32", "64"]))

    def clear_text_area():
        st.session_state['context'] = ""

    if st.button("Save Embeddings"):
        collection = db.get_or_create_collection('context')
        def add_chunk(chunk, sentence):
            embedding = llmmanager.get_embedding(chunk)
            collection.add(ids = [str(uuid.uuid4())], embeddings = [embedding], metadatas = [{'chunk': chunk, 'sentence': sentence, 'source': source}])
        
        for sentence in re.split(r'\.|\n\n', value):
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
        clear_text_area()
