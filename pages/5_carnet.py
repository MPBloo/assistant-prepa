# fichier: pages/5_carnet.py
import streamlit as st
import json
import os
from datetime import datetime




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





st.set_page_config(page_title="📘 Carnet d'erreurs", layout="centered")
st.title("📘 Carnet d'erreurs à revoir")

CHEMIN_ERREURS = "data/carnet_erreurs.json"

# Chargement des erreurs
if not os.path.exists(CHEMIN_ERREURS):
    st.warning("Aucune erreur enregistrée.")
    st.stop()

with open(CHEMIN_ERREURS, encoding="utf-8") as f:
    carnet = json.load(f)

modifications = False

for chapitre, erreurs in carnet.items():
    erreurs_non_reussies = [e for e in erreurs if not e.get("reussi_une_fois")]
    if not erreurs_non_reussies:
        continue

    st.subheader(f"📚 Chapitre : {chapitre}")
    for i, e in enumerate(erreurs_non_reussies):
        with st.expander(f"📝 {e['titre']}"):
            st.markdown(f"**Erreur :** {e['erreur']}")
            st.markdown(f"**Méthode à retenir :** {e['note']}")
            st.markdown(f"**Ajouté le :** {e.get('last_review', 'Inconnu')}")
            # Clé unique : chapitre + titre + index
            key = f"{chapitre}_{e['titre']}_{i}"
            if st.button("✅ Marquer comme réussi une fois", key=key):
                e["reussi_une_fois"] = True
                e["last_success"] = datetime.today().strftime("%Y-%m-%d")
                modifications = True

if modifications:
    with open(CHEMIN_ERREURS, "w", encoding="utf-8") as f:
        json.dump(carnet, f, ensure_ascii=False, indent=2)
    st.success("✅ Carnet mis à jour avec les réussites !")

if not any(e for erreurs in carnet.values() for e in erreurs if not e.get("reussi_une_fois")):
    st.success("🎉 Aucun exercice à revoir : bravo !")
