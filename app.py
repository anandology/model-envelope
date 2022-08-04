"""Streamlit app to view the models.
"""
import json
import streamlit as st
import model_envelope as me

def get_models():
    models = me.list_models()
    data = [[m.id, m.title, m.description, json.dumps(m.tags)] for m in models]
    return data

def add_search():
    with st.form("search"):
        tags = st.text_input("Tags")
        submitted = st.form_submit_button("Search")
    if submitted:
        parts = [p.split("=", 1) for p in tags.split() if "=" in p]
        return dict(parts)
    else:
        return {}

st.title("Models")

tags = add_search()

for m in me.list_models(tags=tags):
    with st.container():
        st.subheader(f"{m.id} - {m.name}")
        st.markdown(m.description)
        tags = "\n".join(f"  {k}={v}" for k, v in m.tags.items())
        st.markdown("**Tags**")
        st.text(tags)
