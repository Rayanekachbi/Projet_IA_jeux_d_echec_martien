Résumé des commandes :
Pour créer un environnement : 

# Windows : 
# Créer l'environnement
python -m venv venv
# Activer l'environnement
.\venv\Scripts\activate

#Mac/Linux : 
# Créer l'environnement
python3 -m venv venv
# Activer l'environnement
source venv/bin/activate

Pour Installer les dépendances et lancer le jeu : 

#Installation : 
pip install -r requirements.txt

#Jouer : 
python src/main.py

#Tournoi : 
python experiments/tournament.py


#Arborescence : 
MartianChess/
│
├── README.md               # Instructions d'installation et règles (Livrable)
│
├── src/                    # Code source principal
│   ├── constants.py        # Configuration globale (tailles, valeurs)
│   ├── model.py            # Structure de l'état du jeu (State)
│   ├── rules.py            # Logique de déplacement et validation
│   ├── view.py             # Interface (Console ou simple GUI)
│   ├── main.py             # Boucle de jeu (Controller)
│   ├── player.py           # Classe parent pour Humains et IA
│   │
│   └── ai/                 # Dossier pour vos IAs
│       ├── minimax.py      # Algorithme Minimax et Alpha-Bêta
│       └── heuristics.py   # Fonctions d'évaluation
│
└── experiments/            # Génération des données pour le rapport
    └── tournament.py       # Script pour lancer 50+ parties IA vs IA