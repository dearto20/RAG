import streamlit as st
import llmmanager

def app():
    st.title('Page 1')
    st.write('문장을 Embedding으로 변환')

    text = st.text_input('Input Text: ')
    if text:
        st.write(llmmanager.get_embedding(text))

