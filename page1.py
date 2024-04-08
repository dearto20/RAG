import streamlit as st
import llmmanager

def main():
    st.title('Convert Sentence to Embedding')
    st.write('Enter Sentence')

    text = st.text_input('Input: ')
    if text:
        st.write(llmmanager.get_embedding(text))
