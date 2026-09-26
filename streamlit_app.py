import streamlit as st

pages = {
    "Mathematical Modules": [
        st.Page("Python Files/logic.py", title="Logic & Proof", url_path="logic"),
        st.Page("Python Files/sets.py", title="Set Operations", url_path="sets"),
        st.Page("Python Files/relations.py", title="Relations & Functions", url_path="relations-functions")
    ]
}

pg = st.navigation(pages)
pg.run()
