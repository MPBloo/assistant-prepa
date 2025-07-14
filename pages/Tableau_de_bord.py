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





st.set_page_config(page_title="📊 Tableau de bord", layout="centered")
st.title("📊 Tableau de bord de votre progression")

# --- Chemins ---
CHEMIN_ERREURS = "data/carnet_erreurs.json"
CHEMIN_REUSSIS = "data/carnet_reussis.json"
DOSSIER_EXOS = "data/exos"

# --- Chargement des données ---
def charger_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def compter_exos_totaux():
    total = {}
    for fichier in os.listdir(DOSSIER_EXOS):
        if fichier.endswith(".json"):
            chemin = os.path.join(DOSSIER_EXOS, fichier)
            with open(chemin, encoding="utf-8") as f:
                data = json.load(f)
                chapitre = fichier.replace(".json", "")
                if "questions_cours" in data:
                    total[chapitre] = len(data["questions_cours"])
                else:
                    total[chapitre] = len(data)
    return total

# --- Données ---
carnet_erreurs = charger_json(CHEMIN_ERREURS)
carnet_reussis = charger_json(CHEMIN_REUSSIS)
total_exos = compter_exos_totaux()

# --- Statistiques générales ---
total_faits = 0
nb_reussis = 0
nb_erreurs = 0

for chapitre in carnet_reussis:
    nb_reussis += len(carnet_reussis[chapitre])
    total_faits += len(carnet_reussis[chapitre])

for chapitre in carnet_erreurs:
    nb_erreurs += len(carnet_erreurs[chapitre])
    total_faits += len(carnet_erreurs[chapitre])

if total_faits > 0:
    taux_reussite = nb_reussis / total_faits * 100
else:
    taux_reussite = 0

st.metric("📌 Exercices faits", total_faits)
st.metric("✅ Exercices réussis", nb_reussis)
st.metric("❌ Exercices en erreur", nb_erreurs)
st.metric("📈 Taux de réussite", f"{taux_reussite:.1f}%")

# --- Temps passé ---
# Utiliser les dates dans carnet_erreurs et carnet_reussis
aujourd_hui = datetime.today().strftime("%Y-%m-%d")
semaine = [(datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

temps_journalier = 0
temps_semaine = 0

for carnet in [carnet_erreurs, carnet_reussis]:
    for chapitre in carnet:
        for e in carnet[chapitre]:
            date = e.get("last_review") or e.get("date_ajout") or ""
            if date == aujourd_hui:
                temps_journalier += 1
            if date in semaine:
                temps_semaine += 1

st.metric("⏱️ Temps passé aujourd'hui (estimation)", f"{temps_journalier * 2} min")
st.metric("📅 Temps cette semaine (estimation)", f"{temps_semaine * 2} min")

# --- Avancement par chapitre ---
st.subheader("📘 Avancement par chapitre")

for chapitre, total in total_exos.items():
    nb_traite = 0
    for source in [carnet_reussis, carnet_erreurs]:
        for c in source:
            if c in chapitre or chapitre in c:
                nb_traite += len(source[c])
    pourcentage = min(100, int(nb_traite / total * 100)) if total else 0
    st.markdown(f"**{chapitre}**")
    st.progress(pourcentage, text=f"{nb_traite}/{total} exercices faits")
