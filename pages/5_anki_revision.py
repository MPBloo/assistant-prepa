import streamlit as st
import json
import os
from datetime import datetime, timedelta








from datetime import datetime
if "session_en_cours" in st.session_state and st.session_state.session_en_cours:
    temps_restant = st.session_state.fin_session - datetime.now()
    if temps_restant.total_seconds() > 0:
        minutes, secondes = divmod(int(temps_restant.total_seconds()), 60)
        st.sidebar.info(f"⏳ {minutes} min {secondes} sec restants")
    else:
        st.sidebar.warning("⏳ Temps écoulé.")
        st.session_state.session_en_cours = False
        st.session_state.fin_session = None





st.set_page_config(page_title="🔁 Révisions intelligentes", layout="centered")
st.title("🔁 Révision ciblée (Anki-style)")

# --- Chargement du carnet d'erreurs ---
CHEMIN_ERREURS = "data/carnet_erreurs.json"

def charger_erreurs():
    if not os.path.exists(CHEMIN_ERREURS):
        return {}

    with open(CHEMIN_ERREURS, encoding="utf-8") as f:
        carnet = json.load(f)

    # Mise à jour des anciennes erreurs pour ajouter les champs Anki si manquants
    today = datetime.today().strftime("%Y-%m-%d")
    for chapitre in carnet:
        for entry in carnet[chapitre]:
            if "repetitions" not in entry:
                entry["repetitions"] = 0
            if "interval" not in entry:
                entry["interval"] = 1
            if "ease" not in entry:
                entry["ease"] = 2.5
            if "last_review" not in entry:
                entry["last_review"] = today
            if "due_date" not in entry:
                entry["due_date"] = today

    return carnet

def sauvegarder_erreurs(data):
    with open(CHEMIN_ERREURS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def est_due(entry):
    return datetime.strptime(entry["due_date"], "%Y-%m-%d") <= datetime.today()

def prochaine_date(interval):
    return (datetime.today() + timedelta(days=interval)).strftime("%Y-%m-%d")

def maj_espacement(entry, reussite):
    if reussite:
        entry["repetitions"] += 1
        entry["ease"] = max(1.3, entry["ease"] + 0.1)
        entry["interval"] = int(entry["interval"] * entry["ease"])
    else:
        entry["repetitions"] = 0
        entry["ease"] = max(1.3, entry["ease"] - 0.2)
        entry["interval"] = 1
    entry["last_review"] = datetime.today().strftime("%Y-%m-%d")
    entry["due_date"] = prochaine_date(entry["interval"])

# --- Logique principale ---
carnet = charger_erreurs()
exos_du = []
for chapitre, erreurs in carnet.items():
    for e in erreurs:
        if est_due(e):
            exos_du.append((chapitre, e))

if not exos_du:
    st.success("✅ Aucune révision due aujourd'hui !")
    st.stop()

# --- Affichage d'une révision ---
st.subheader("📌 À revoir aujourd'hui")
chapitre, exo = exos_du[0]
st.markdown(f"**Chapitre :** {chapitre}")
st.markdown(f"**Exercice :** {exo['titre']}")

# Affichage de l'énoncé si disponible
if "question" in exo:
    st.markdown("**Énoncé :**")
    st.markdown(exo["question"], unsafe_allow_html=True)
else:
    st.info("Aucun énoncé n'est disponible pour cet exercice.")

col1, col2 = st.columns(2)
with col1:
    if st.button("✅ J'ai réussi"):
        maj_espacement(exo, reussite=True)
        sauvegarder_erreurs(carnet)
        st.rerun()
with col2:
    if st.button("❌ Encore raté"):
        maj_espacement(exo, reussite=False)
        sauvegarder_erreurs(carnet)
        st.rerun()
