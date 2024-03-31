import streamlit as st
import page1, page2

PAGES = {
    "Page 1": page1,
    "Page 2": page2
}

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.app()

if __name__ == "__main__":
    main()

