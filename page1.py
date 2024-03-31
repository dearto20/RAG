import streamlit as st
import llm_manager

def app():
    st.title('Page 1')
    st.write('This is page 1')

    text = st.text_input('Input Text: ')
    if text:
        embedding = llm_manager.get_embedding(text)
        st.write(embedding)

