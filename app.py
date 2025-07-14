import streamlit as st

st.set_page_config(page_title="Coach prépa", layout="centered")
st.title("Bienvenue dans l'assistant prépa 🧠")

st.markdown("""
### Choisissez une page dans le menu à gauche :
- 📘 Accueil : pour commencer votre séance de rappels
- 🧠 Rappels : pour faire les questions du jour
""")


if "page" not in st.session_state:
    st.session_state.page = "accueil"

if st.session_state.page == "accueil":
    st.title("Page d’accueil")
    if st.button("Allons-y !"):
        st.session_state.page = "rappels"
        st.rerun()
