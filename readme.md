# LITReview — Projet Django

## Description

LITReview est une application Django permettant de publier des billets, écrire des critiques, suivre des utilisateurs et afficher un flux social personnalisé.

---

## Prérequis

- Python 3.9 ou supérieur
- pip
- Un environnement virtuel Python

---

## Installation locale

1. **Cloner le dépôt**
git clone [<URL_DU_DEPOT>](https://github.com/Americanufo/Projet_9.git)
cd LITReview

2. **Créer un environnement virtuel et l’activer**
python -m venv env
source env/bin/activate # Windows : env\Scripts\activate

3. **Installer les dépendances**
pip install -r requirements.txt

Le fichier `requirements.txt` contient toutes les dépendances nécessaires (par ex. Django, Pillow).

4. **Configurer la base de données**
- Par défaut, le projet utilise SQLite (configuration dans `settings.py`) : aucun paramétrage supplémentaire n’est nécessaire.

5. **Lancer les migrations**
python manage.py migrate

Cela crée toutes les tables nécessaires dans la base.

6. **Créer un super-utilisateur pour accéder à l’admin**
python manage.py createsuperuser

7. **Démarrer le serveur de développement**
python manage.py runserver
Accéder à l’application via [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Étapes pour sécuriser la clé secrète

La clé secrète Django (`SECRET_KEY`) est une donnée sensible qui ne doit jamais être exposée publiquement.

### 1. Créer un fichier `.env`

Crée un fichier `.env` à la racine de ton projet (là où se trouve le fichier `manage.py`).

- **Sur macOS ou Linux :**

  Ouvre le terminal, navigue dans ton projet puis crée le fichier avec un éditeur de texte (exemple : nano) :
  cd /chemin/vers/ton/projet
  nano .env

- **Sur Windows :**

Ouvre le Bloc-notes (Notepad) ou un autre éditeur de texte, puis crée un fichier nommé `.env` (avec un point au début, pas d'extension) à la racine du projet.

---

### 2. Ajouter la clé secrète dans `.env`

Dans ce fichier `.env`, ajoute la ligne suivante (remplace la clé par ta propre clé secrète) :

SECRET_KEY=ta_clef_secrete_django_ici

Sauvegarde et quitte l’éditeur (`Ctrl+O` puis `Entrée` et `Ctrl+X` dans nano).

---

### 3. Ajouter `.env` au `.gitignore`

Pour éviter que le fichier `.env` soit poussé dans ton dépôt git et exposé publiquement, ajoute `.env` à ton `.gitignore` :


---

### 4. Installer la librairie `python-decouple`

Cette librairie permet de charger automatiquement les variables depuis `.env`.

Installe-la avec :
pip install python-decouple

---

### 5. Modifier `settings.py`

Dans ton fichier `settings.py`, importe `config` depuis `decouple` en ajoutant en haut :
from decouple import config

Puis remplace la ligne contenant la clé statique par :

SECRET_KEY = config('SECRET_KEY')

---

## Organisation du projet

- `blog/` : application principale pour la gestion des billets, critiques et flux.
- `authentication/` : gestion des utilisateurs et abonnements.
- `templates/` : fichiers HTML
- `static/` : fichiers CSS, JS, images statiques

---
## Fichiers importants

- `requirements.txt` : contient toutes les dépendances Python du projet
- `manage.py` : outil de gestion de Django (migrations, serveur, etc.)
- `settings.py` : configuration générale, notamment la base de données et fichiers médias

---

## Notes supplémentaires

- Pour gérer les images, `Pillow` est requis.
- Pensez à utiliser un environnement virtuel pour éviter les conflits.
- Toute modification des modèles nécessite de lancer `makemigrations` puis `migrate`.
- Pour supprimer un utilisateur, utilisez l’interface Django Admin (accessible via `/admin`).



