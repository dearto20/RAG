import streamlit as st
import page3, page4

PAGES = {
    "Personal Context Management": page3,
    "Find Out Matching Context": page4,
}

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Pages", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.app()

if __name__ == "__main__":
    main()
