import json
import os

CHEMIN_REUSSIS = "data/carnet_reussis.json"

def charger_json(chemin):
    if not os.path.exists(chemin):
        return {}
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_json(chemin, data):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def ajouter_reussi(chapitre, titre, note):
    data = charger_json(CHEMIN_REUSSIS)

    if chapitre not in data:
        data[chapitre] = []

    # Vérifie si l’exercice est déjà présent
    deja_present = any(e["titre"] == titre for e in data[chapitre])
    if not deja_present:
        data[chapitre].append({
            "titre": titre,
            "note": note
        })

    sauvegarder_json(CHEMIN_REUSSIS, data)
