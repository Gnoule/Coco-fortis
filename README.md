# Coco-fortis - Constraint Learning from Abstraction and Reasoning Corpus (ARC)

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
- `pycsp3` : solveur de contraintes (CHOCO).
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
git clone https://github.com/Gnoule/Coco-fortis.git
cd Coco-fortis

# Créer un environnement
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Contraintes extraites automatiquement

Le système peut détecter plusieurs types de contraintes symboliques :

| Contrainte                       | Description                                                             |
|----------------------------------|-------------------------------------------------------------------------|
| `GRID_SIZE`                      | Taille de la grille de sortie                                           |
| `FORM_INPUT_EQUAL_FORM_OUTPUT`   | Conservation d’une forme présente dans l’entrée                         |
| `FORM_OUTPUT_COLOR`              | Couleur attendue pour une forme donnée                                  |
| `NUMBER_NODES_OUTPUT`            | Nombre total de formes attendues en sortie                              |
| `NODE_X_FIXED` / `NODE_Y_FIXED`  | Blocage du déplacement d’un objet selon l’axe **X** ou **Y**            |
| `CENTER_NODE`                    | Imposition d’un positionnement central                                  |
| `KEEP_NODE`                      | Obligation de conserver certaines structures                            |
| `EXTEND_TO_NODE`                 | Extension d’une forme vers une autre forme voisine                      |

## Sources

- François Chollet, [Abstraction and Reasoning Corpus (ARC)](https://github.com/fchollet/ARC)
- [PyCSP3](https://pycsp.org) — Langage de modélisation pour les problèmes de satisfaction de contraintes
- Guernout et al., *A Neuro-Symbolic Approach for Program Synthesis from Visual Examples (2022)* — [PDF](https://arxiv.org/pdf/2210.09880)
- François Chollet, *The Measure of Intelligence (2019)* — [PDF](https://arxiv.org/pdf/1911.01547)
- [ARGA: Abductive Reasoning Graph Abstraction for Solving ARC Tasks](https://github.com/khalil-research/ARGA-AAAI23) — Implémentation du papier ARGA (AAAI 2023)

Projet développé par Mathéo et Hugo dans le cadre d’un stage en recherche d'un durée de un mois sur l'apprentissage de contraintes logiques.
