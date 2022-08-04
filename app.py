"""Streamlit app to view the models.
"""
import json
import streamlit as st
import model_envelope as me

def get_models():
    models = me.list_models()
    data = [[m.id, m.title, m.description, json.dumps(m.tags)] for m in models]
    return data

st.title("Models")

for m in me.list_models():
    with st.container():
        st.subheader(f"{m.id} - {m.name}")
        st.markdown(m.description)
        tags = "\n".join(f"  {k} = {v}" for k, v in m.tags.items())
        st.markdown("**Tags**")
        st.write(tags)
