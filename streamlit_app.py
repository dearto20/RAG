import streamlit as st
import page1, page2, page3, page4

PAGES = {
    #"Convert Sentence into Embedding": page1,
    #"Compare Similarity Using Embedding": page2,
    "Put Contexts Into RAG DB": page3,
    "Query Matching Context": page4,
}

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.app()

if __name__ == "__main__":
    main()
