import streamlit as st
import page3, page4, page5, page6

PAGES = {
    "Manage Personal Context in DB": page3,
    "Ask LLM with Personal Context": page4,
    "(Llamaindex) Manage Personal Context in DB": page5,
    "(Llamaindex) Ask LLM with Personal Context": page6,
}

def main():
    st.sidebar.title('Indexing and Query Test With or Without Llamaindex')
    selection = st.sidebar.radio("Pages", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.app()

if __name__ == "__main__":
    main()
