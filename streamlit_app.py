import streamlit as st
import page1, page2, page3, page4

PAGES = {
    "Context Indexing and Storing": page1,
    "Context Retrieval and Querying": page2,
    "(w/Llamaindex) Context Indexing and Storing": page3,
    "(w/Llamaindex) Context Retrieval and Querying": page4,
}

def main():
    st.sidebar.title('Retrieve and Query Context With or Without Llamaindex')
    selection = st.sidebar.radio("Pages", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.app()

if __name__ == "__main__":
    main()
