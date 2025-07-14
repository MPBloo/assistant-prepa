import streamlit as st
import json
import os
from datetime import datetime

import streamlit as st
from datetime import datetime
from memoire_manager import charger_donnees, mettre_a_jour_revision, rappels_du_jour, sauvegarder_donnees
import time

st.set_page_config(page_title="🔁 Rappels du jour", layout="centered")
st.title("🔁 Révision active : rappels du jour")

# Chargement des données
donnees = charger_donnees()
rappels = rappels_du_jour(donnees)

# Initialisation de la session
if "rappel_index" not in st.session_state:
    st.session_state.rappel_index = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Affichage de la question actuelle
if st.session_state.rappel_index < len(rappels):
    fiche_id = rappels[st.session_state.rappel_index]["id"]
    fiche = next((f for f in donnees if f["id"] == fiche_id), None)

    if fiche:
        st.subheader(f"Question {st.session_state.rappel_index + 1} sur {len(rappels)}")
        st.markdown(f"**{fiche['contenu']}**")

        elapsed = int(time.time() - st.session_state.start_time)
        st.info(f"⏱ Temps écoulé : {elapsed} secondes")

        if st.button("📖 Voir la réponse"):
            st.success(fiche["reponse"])

        st.markdown("Avez-vous trouvé la bonne réponse ?")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Oui"):
                mettre_a_jour_revision(fiche, True)
                sauvegarder_donnees(donnees)
                st.session_state.rappel_index += 1
                st.session_state.start_time = time.time()
                st.rerun()

        with col2:
            if st.button("❌ Non"):
                mettre_a_jour_revision(fiche, False)
                sauvegarder_donnees(donnees)
                st.session_state.rappel_index += 1
                st.session_state.start_time = time.time()
                st.rerun()
    else:
        st.error("❌ Fiche non trouvée.")
else:
    st.success("🎉 Tous les rappels du jour ont été effectués !")
    if st.button("Retour à l'accueil"):
        st.switch_page("pages/1_accueil.py")
