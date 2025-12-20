from pathlib import Path

import streamlit as st

st.set_page_config(page_title="i-Scope", layout="wide")

PAGE_LABELS = {
    "error_analysis": "Error Analysis",
    "test_execution": "Test Execution",
    "case_search": "Case Search",
}


def load_pages():
    pages_dir = Path(__file__).parent / "pages"
    page_list = []
    for page_path in sorted(pages_dir.glob("*.py")):
        stem = page_path.stem
        title = PAGE_LABELS.get(stem, stem.replace("_", " ").title())
        page_list.append(st.Page(str(page_path.resolve()), title=title))
    return page_list


pages = load_pages()
if not pages:
    st.error("앱에서 표시할 페이지가 없습니다.")
else:
    navigation = st.navigation(pages)
    navigation.run()
