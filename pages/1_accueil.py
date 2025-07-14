import streamlit as st
from datetime import datetime, timedelta
from memoire_manager import charger_donnees, rappels_du_jour

st.set_page_config(page_title="🏠 Accueil", layout="centered")

# Charger les données de mémoire
donnees = charger_donnees()
rappels = rappels_du_jour(donnees)

# Initialisation du timer
if "session_en_cours" not in st.session_state:
    st.session_state.session_en_cours = False
if "fin_session" not in st.session_state:
    st.session_state.fin_session = None

# Affichage du nombre de rappels à faire
st.markdown(f"<h1 style='text-align: center; color: #4B8BBE;'>🧠 {len(rappels)} rappels à réviser</h1>", unsafe_allow_html=True)

# Choix de la durée de la session si pas encore commencée
if not st.session_state.session_en_cours:
    duree = st.selectbox("⏱️ Choisissez la durée de votre session :", ["30 min", "1 h", "2 h"])
    if st.button("🚀 Commencer la session"):
        minutes = {"30 min": 30, "1 h": 60, "2 h": 120}[duree]
        st.session_state.fin_session = datetime.now() + timedelta(minutes=minutes)
        st.session_state.session_en_cours = True
        st.success("✅ Session démarrée !")
        st.rerun()
else:
    # Affichage du chronomètre si session en cours
    temps_restant = st.session_state.fin_session - datetime.now()
    if temps_restant.total_seconds() <= 0:
        st.session_state.session_en_cours = False
        st.session_state.fin_session = None
        st.warning("⏳ Temps écoulé. Fin de la session.")
    else:
        minutes, secondes = divmod(int(temps_restant.total_seconds()), 60)
        st.info(f"🕒 Temps restant : {minutes} min {secondes} sec")

# Deux boutons côte à côte
col1, col2 = st.columns(2)

with col1:
    if st.button("🧠 Faire les rappels"):
        st.session_state["debut_session"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["q_index"] = 0
        st.switch_page("pages/2_rappels.py")

with col2:
    if st.button("📘 Je veux faire des exercices"):
        st.switch_page("pages/3_exos.py")

# Message de motivation
st.markdown("---")
st.markdown("💡 *“Celui qui progresse un peu chaque jour ira loin. Courage !”*")
