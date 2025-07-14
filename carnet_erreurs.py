import json
import os
from datetime import datetime

CARNET_PATH = "data/carnet_erreurs.json"

# --- Chargement du carnet d'erreurs ---
def charger_carnet():
    if not os.path.exists(CARNET_PATH):
        return {}
    with open(CARNET_PATH, encoding="utf-8") as f:
        return json.load(f)

# --- Sauvegarde ---
def sauvegarder_carnet(carnet):
    with open(CARNET_PATH, "w", encoding="utf-8") as f:
        json.dump(carnet, f, ensure_ascii=False, indent=2)

# --- Ajout d'une erreur avec métadonnées pour la révision espacée ---
def ajouter_erreur(chapitre, exo, erreur, methode, question):
    carnet = charger_carnet()
    if chapitre not in carnet:
        carnet[chapitre] = []
    carnet[chapitre].append({
        "titre": exo,
        "erreur": erreur,
        "note": methode,
        "question": question,
        "corrige": False,
        "date_ajout": datetime.now().strftime("%Y-%m-%d")
    })
    sauvegarder_carnet(carnet)


# --- Marquer une erreur comme corrigée (optionnel si vous avez un affichage manuel) ---
def marquer_comme_corrige(chapitre, index):
    carnet = charger_carnet()
    if chapitre in carnet and 0 <= index < len(carnet[chapitre]):
        carnet[chapitre][index]["corrige"] = True
        sauvegarder_carnet(carnet)

# --- Utilitaires ---
def chapitres_disponibles():
    carnet = charger_carnet()
    return list(carnet.keys())

def erreurs_du_chapitre(chapitre):
    carnet = charger_carnet()
    return carnet.get(chapitre, [])
