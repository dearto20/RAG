import streamlit as st
import llmmanager

def app():
    st.title('Page 1')
    st.write('This is page 1')

    text = st.text_input('Input Text: ')
    if text:
        #embedding = llmmanager.get_embedding(text)
        #st.write(embedding)
        st.write(text)

