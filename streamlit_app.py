import streamlit as st
import page1, page2, page3, page4

PAGES = {
    "Index Personal Context in the Local DB": page1,
    "Retrieve Personal Context and Query LLM": page2,
    "(w/Llamaindex) Index Personal Context in the Local DB": page3,
    "(w/Llamaindex) Retrieve Personal Context and Query LLM": page4,
}

def main():
    st.sidebar.title('Indexing and Querying Context With or Without Llamaindex')
    selection = st.sidebar.radio("Pages", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.app()

if __name__ == "__main__":
    main()
