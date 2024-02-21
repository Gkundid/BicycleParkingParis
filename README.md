# Titre du Projet

Description courte du projet.

## Configuration de l'Environnement de Développement

Ce projet nécessite Python et Node.js. Voici comment configurer votre environnement de développement.

### Backend (Python)

1. Assurez-vous d'avoir Python installé sur votre machine. Ce projet utilise Python 3.8+.

2. Créez un environnement virtuel dans le dossier backend :
    ```bash
    cd backend
    python -m venv venv
    ```

3. Activez l'environnement virtuel :
    - Sur Windows :
        ```bash
        .\venv\Scripts\activate
        ```
    - Sur macOS et Linux :
        ```bash
        source venv/bin/activate
        ```

4. Installez les dépendances nécessaires :
    ```bash
    pip install -r requirements.txt
    ```

### Frontend (Node.js)

1. Assurez-vous d'avoir Node.js et npm installés.

2. Installez les dépendances du projet :
    ```bash
    cd frontend
    npm install
    ```

## Exécution du Projet

### Backend

Pour lancer le serveur backend, exécutez :
```bash
python server.py
