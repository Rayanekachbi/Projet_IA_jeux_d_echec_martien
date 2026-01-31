MartianChess/
│
├── README.md               # Instructions d'installation et règles (Livrable)
├── run.sh                  # Script de lancement (Livrable)
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
│       ├── minimax.py      # L'algorithme Minimax et Alpha-Bêta
│       └── heuristics.py   # Vos différentes fonctions d'évaluation
│
├── tests/                  # Tests unitaires (Bonus)
│   ├── test_rules.py
│   └── test_state.py
│
└── experiments/            # Pour générer les données du rapport 
    └── tournament.py       # Script pour lancer 50+ parties IA vs IA
