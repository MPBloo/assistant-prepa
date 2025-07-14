import streamlit as st
import json
import os
import re
from datetime import datetime

from carnet_erreurs import ajouter_erreur
from carnet_reussis import ajouter_reussi

# --- Timer session ---
if "session_en_cours" in st.session_state and st.session_state.session_en_cours:
    temps_restant = st.session_state.fin_session - datetime.now()
    if temps_restant.total_seconds() > 0:
        minutes, secondes = divmod(int(temps_restant.total_seconds()), 60)
        st.sidebar.info(f"⏳ {minutes} min {secondes} sec restants")
    else:
        st.sidebar.warning("⏳ Temps écoulé.")
        st.session_state.session_en_cours = False
        st.session_state.fin_session = None

st.set_page_config(page_title="🧠 Exercices guidés", layout="centered")
st.title("🧠 Séance d'entraînement guidée")

# --- Choix du chapitre ---
chapitres_disponibles = {
    "Induction (cours)": "data/exos/induction_questions_cours.json",
    "Induction (exos)": "data/exos/induction.json",
    "Continuité": "data/exos/continuite.json",
    "Complexes": "data/exos/nombres_complexes.json"
}
chapitre = st.selectbox("📘 Choisissez un chapitre :", list(chapitres_disponibles.keys()))

# --- Chargement des données JSON ---
chemin = chapitres_disponibles[chapitre]
if not os.path.exists(chemin):
    st.warning(f"Aucun fichier trouvé pour le chapitre : {chapitre}")
    st.stop()

with open(chemin, encoding="utf-8") as f:
    data = json.load(f)

# Identifier si c'est un fichier de cours ou d'exercices
if "questions_cours" in data:
    elements = data["questions_cours"]
    est_cours = True
else:
    elements = data
    est_cours = False

# --- Initialisation session ---
if "exo_index" not in st.session_state:
    st.session_state.exo_index = 0
if "reponse_exo" not in st.session_state:
    st.session_state.reponse_exo = None

# --- Nettoyage et affichage intelligent ---
def nettoyer_question(texte):
    if not isinstance(texte, str):
        return texte
    texte = texte.replace("\\\\", "\\")
    texte = texte.replace("\\ ", " ")
    texte = re.sub(r"\\\(|\\\)", "", texte)
    texte = re.sub(r"\\[^\w]", "", texte)
    texte = re.sub(r"\s{2,}", " ", texte)
    return texte.strip()

def afficher_mixte(texte):
    texte = nettoyer_question(texte)
    if any(sym in texte for sym in ["^", "_", "=", "\\frac", "+", "-", "|", "\\times"]):
        try:
            st.latex(texte)
        except:
            st.markdown(texte)
    else:
        st.markdown(texte)

# --- Affichage de l'exercice ---
if st.session_state.exo_index < len(elements):
    item = elements[st.session_state.exo_index]

    if est_cours:
        st.subheader(f"Question {st.session_state.exo_index + 1}")
        st.markdown("**Énoncé :**")
        afficher_mixte(item["question"])
        if st.button("✅ Voir la réponse"):
            st.markdown("**Réponse :**")
            afficher_mixte(item["reponse"])
    else:
        st.subheader(f"Exercice {st.session_state.exo_index + 1} : {item['titre']}")
        st.markdown("**Énoncé :**")
        afficher_mixte(item["question"])
        if st.button("💡 Voir un indice"):
            st.markdown("**Indice :**")
            afficher_mixte(item["indice"])
        if st.button("✅ Voir la solution"):
            st.markdown("**Solution :**")
            afficher_mixte(item["solution"])

    st.markdown("---")

    # Choix réussite/échec
    st.markdown("**Avez-vous réussi cet exercice ?**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Oui, réussi"):
            st.session_state.reponse_exo = "oui"
    with col2:
        if st.button("❌ Non, encore raté"):
            st.session_state.reponse_exo = "non"

    # Réussite
    if st.session_state.reponse_exo == "oui":
        note = st.text_input("✅ Quelle méthode retenez-vous ?", key=f"note_{st.session_state.exo_index}")
        if st.button("➡️ Suivant", key=f"suivant_{st.session_state.exo_index}_reussi"):
            if note:
                titre = item.get("titre", item["question"][:50])
                ajouter_reussi(chapitre, titre, note)
                st.session_state.reponse_exo = None
                st.session_state.exo_index += 1
                st.rerun()
            else:
                st.warning("Merci d’écrire une méthode à retenir.")

    # Échec
    elif st.session_state.reponse_exo == "non":
        erreur = st.text_input("❌ Quelle erreur avez-vous faite ?", key=f"err_{st.session_state.exo_index}")
        methode = st.text_input("✅ Quelle méthode retenir ?", key=f"methode_{st.session_state.exo_index}")
        if st.button("➡️ Suivant", key=f"suivant_{st.session_state.exo_index}_rate"):
            if erreur and methode:
                titre = item.get("titre", item["question"][:50])
                ajouter_erreur(chapitre, titre, erreur, methode, item["question"])
                st.session_state.reponse_exo = None
                st.session_state.exo_index += 1
                st.rerun()
            else:
                st.warning("Merci de remplir les deux champs.")
else:
    st.success("🎉 Vous avez terminé tous les éléments de ce chapitre.")
    if st.button("Retour à l’accueil"):
        st.switch_page("pages/1_accueil.py")
