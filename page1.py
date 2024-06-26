import streamlit as st
import llmmanager
import uuid
import re

def app():
    db = llmmanager.get_database()

    st.header('Manage the Context in the Database')
    st.write('Remove All Embeddings in the Database')
    if st.button("Reset the Database"):
        try:
            db.delete_collection('context')
        except ValueError:
            pass
        st.toast('Finished')
    
    st.divider()
    st.write('Enter New Context to Add to the Database')

    context = st.text_area('Context', height = 196)
    source = st.selectbox('Source', ('KG', 'Runestone', 'Etc'))
    chunk_size = int(st.radio("Chunk Size", ["256", "512", "1024"]))

    st.write('Convert the Context into Embeddings and Save')
    if st.button("Save to the Database"):
        collection = db.get_or_create_collection('context')
        def add_chunk(chunk, sentence):
            embedding = llmmanager.get_embedding(chunk)
            collection.add(ids = [str(uuid.uuid4())], embeddings = [embedding], metadatas = [{'chunk': chunk, 'sentence': sentence, 'source': source}])

        count = 0
        for sentence in re.split(r'\.|\n\n', context):
            sentence = re.sub(r'\s{2, }', ' ', sentence).strip()
            if not sentence:
                continue

            count = count + 1
            #st.write(f'Sentence {count}: {sentence}')
            #add_chunk(sentence, sentence)

            if chunk_size > 0:
                words = re.findall(r'\S+', sentence)
                index = 0
                while cur_words := words[index:index + chunk_size]:
                    index += chunk_size - (chunk_size // 4)
                    chunk = ' '.join(cur_words)
                    st.write(f'Chunk: {chunk}')
                    add_chunk(chunk, sentence) 
        st.toast('Saved')
