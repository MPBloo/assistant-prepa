import streamlit as st
import json
import os




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




st.set_page_config(page_title="✅ Exercices réussis", layout="centered")
st.title("✅ Vos réussites")

CHEMIN_ERREURS = "data/carnet_erreurs.json"
CHEMIN_REUSSIS = "data/carnet_reussis.json"

def charger_json(chemin):
    if not os.path.exists(chemin):
        return {}
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_json(chemin, data):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Chargement des exercices réussis
carnet_reussis = charger_json(CHEMIN_REUSSIS)

if not carnet_reussis:
    st.info("Aucun exercice n'a encore été marqué comme réussi.")
else:
    for chapitre, exos in carnet_reussis.items():
        if exos:
            st.subheader(f"📘 {chapitre}")
            for exo in exos:
                st.markdown(f"**Exercice :** {exo['titre']}")
                st.markdown(f"**Méthode retenue :** {exo['note']}")
                st.markdown("---")
