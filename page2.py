import streamlit as st
import llmmanager

def app():
    text1 = st.text_input('Source')
    text2 = st.text_input('Target')

    if text1 and text2:
        embedding1 = llmmanager.get_embedding(text1)
        embedding2 = llmmanager.get_embedding(text2)
        st.write('Similarity: ', llmmanager.get_distance(embedding1, embedding2))

