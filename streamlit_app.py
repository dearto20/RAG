import streamlit as st
import page1, page2, page3, page4

PAGES = {
    "Manage Personal Context in DB": page1,
    "Ask LLM with Personal Context": page2,
    "(w/Llamaindex) Manage Personal Context in DB": page3,
    "(w/Llamaindex) Ask LLM with Personal Context": page4,
}

def main():
    st.sidebar.title('Indexing and Query Test With or Without Llamaindex')
    selection = st.sidebar.radio("Pages", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.app()

if __name__ == "__main__":
    main()
