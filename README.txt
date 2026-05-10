# MartianChess

## Auteurs

Ce projet a été réalisé par :

- Rayan KACHBI
- Yanis HAMMAOUI


Année universitaire : 2025–2026

---

## Présentation
...


## Arborescence du projet

Projet_IA_jeux_d_echec_martien/
│
├── README.md               # Instructions d'installation et règles (Livrable)
│
├── src/                    # Code source principal
│   ├── __init__.py
│   ├── constants.py        # Configuration globale (tailles, valeurs)
│   ├── model.py            # Structure de l'état du jeu (State)
│   ├── rules.py            # Logique de déplacement et validation
│   ├── view.py             # Interface (Console ou simple GUI)
│   ├── game.py             # Boucle de jeu (Controller)
│   ├── player.py           # Classe parent pour Humains et IA
│   │
│   └── ai/                 # Dossier pour vos IAs
│       ├── __init__.py
│       ├── minimax.py      # Algorithme Minimax et Alpha-Bêta
│       └── heuristics.py   # Fonctions d'évaluation
│
│
└── experiments/            # Génération des données pour le rapport
    └── tournament.py       # Script pour lancer 50+ parties IA vs IA

## Instructions d'exécution
A la racine du projet

### 1. Créer et activer un environnement virtuel

Sous Linux / macOS :

```bash
python3 -m venv venv
source venv/bin/activate
```

Sous Windows :

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer le jeu

```bash
python src/main.py
```

### 5. Lancer les expérimentations IA vs IA

```bash
python -m experiments.tournament
```