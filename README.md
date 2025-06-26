# Coco-fortis

Ce projet vise à **apprendre automatiquement des contraintes logiques** à partir d’exemples d’entrées/sorties visuelles, dans le style des tâches de l’**Abstraction and Reasoning Corpus (ARC)**. Il s’appuie sur une **représentation par graphes** et une **résolution via CSP (Problème de Satisfaction de Contraintes)**.

---

## Objectif

Le but est de généraliser à partir de quelques exemples visuels (images) en extrayant automatiquement des règles **symboliques** comme :
- La **conservation de formes** (rectangles, structures colorées).
- La **transformation géométrique** (translation, suppression, recoloration).
- L’utilisation de ces règles dans un solveur CSP pour produire une sortie correcte sur des cas non vus.

---

## Architecture

### Dossiers
- `main/` : code principal contenant les modules :
  - `Graph.py` : construction des graphes à partir des grilles.
  - `Nodes.py` : définition des nœuds (objets formés de pixels connectés).
  - `ConstraintFinder.py` : fonctions pour analyser les paires input/output.
  - `ConstraintResolver.py` : génération et écriture des contraintes CSP (PyCSP3).
  - `ResolverFromCP.py` : reconstruction de l'image à partir de la sortie du solveur.
  - `Main.py` : script principal de test.

### Dépendances
- `pycsp3` : solveur de contraintes (ACE).
- `networkx`, `matplotlib`, `numpy` : visualisation et traitement.
- Python 3.10+ conseillé.

---

## Exemple de fonctionnement

Dans `Main.py`, le script :
1. Charge les exemples `train` et `test` depuis un fichier JSON.
2. Construit un graphe à partir des images d’entrée.
3. Analyse les correspondances et extrait des règles.
4. Résout un modèle CSP pour appliquer les règles aux nouvelles entrées.
5. Affiche la grille d’origine et la grille prédite.

---

## Installation

```bash
git clone https://github.com/ton-utilisateur/ton-projet.git
cd ton-projet

# Créer un environnement
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Installer les dépendances
pip install -r requirements.txt
