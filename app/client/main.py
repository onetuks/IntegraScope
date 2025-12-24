import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

st.set_page_config(page_title="i-Scope", layout="wide")

NAV_TITLE = "I-Scope"

PAGE_LABELS = {
    "artifact_search": "Artifact Search",
    "tested_list": "Tested Artifacts",
}


def load_pages():
    pages_dir = Path(__file__).parent / "pages"
    page_list = []
    for page_path in sorted(pages_dir.glob("*.py")):
        if "__init__.py" in page_path.name:
            continue
        if "analysis.py" in page_path.name:
            continue
        stem = page_path.stem
        title = PAGE_LABELS.get(stem, stem.replace("_", " ").title())
        page_list.append(st.Page(str(page_path.resolve()), title=title))
    return page_list


pages = load_pages()
if not pages:
    st.error("앱에서 표시할 페이지가 없습니다.")
else:
    st.sidebar.markdown(f"### {NAV_TITLE}")
    navigation = st.navigation(pages)
    navigation.run()
