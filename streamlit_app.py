import streamlit as st
import page1, page2, page3, page4

PAGES = {
    "Manage Personal Context in the Local DB": page1,
    "Retrieve Personal Context and Query LLM": page2,
    "(w/Llamaindex) Manage Personal Context in the Local DB": page3,
    "(w/Llamaindex) Retrieve Personal Context and Query LLM": page4,
}

def main():
    st.sidebar.title('Retrieve and Query Personal Context With or Without Llamaindex')
    selection = st.sidebar.radio("Pages", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.app()

if __name__ == "__main__":
    main()
