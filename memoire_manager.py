import json
from datetime import datetime, timedelta
from typing import List, Dict

MEMOIRE_PATH = "data/memoire.json"

# Chargement et sauvegarde des données
def charger_donnees(path: str = MEMOIRE_PATH) -> List[Dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_donnees(donnees: List[Dict], path: str = MEMOIRE_PATH):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=2, ensure_ascii=False)

# Récupération des rappels prévus aujourd'hui
def rappels_du_jour(donnees: List[Dict]) -> List[Dict]:
    aujourd_hui = datetime.today().date()
    return [d for d in donnees if datetime.strptime(d["prochaine_revision"], "%Y-%m-%d").date() <= aujourd_hui]

# Mise à jour des réussites et recalcul du prochain rappel
def mettre_a_jour_revision(fiche: Dict, reussite: bool):
    fiche["derniere_revision"] = datetime.today().strftime("%Y-%m-%d")
    fiche["reussite"] = reussite

    if reussite:
        fiche["intervalle"] = min(fiche["intervalle"] * 2, 60)  # espacement maximum à 60 jours
    else:
        fiche["intervalle"] = 1

    prochaine = datetime.today() + timedelta(days=fiche["intervalle"])
    fiche["prochaine_revision"] = prochaine.strftime("%Y-%m-%d")

# Historique simplifié (nombre de révisions/jour)
def historique_revisions(donnees: List[Dict], jours: int = 14) -> Dict[str, int]:
    historique = { (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d"): 0 for i in range(jours) }
    for d in donnees:
        date = d.get("derniere_revision")
        if date in historique:
            historique[date] += 1
    return historique
