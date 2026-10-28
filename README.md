# Video Downloader (TokyVideo)

Ce projet permet de télécharger des vidéos depuis TokyVideo en extrayant l'URL directe du flux MP4 à partir du code source de la page.

## Fonctionnalités

- Récupération du code source HTML d'une page TokyVideo.
- Extraction automatique de l'URL MP4 avec jeton de sécurité.
- Téléchargement avec barre de progression (`tqdm`).
- Gestion de la reprise du téléchargement en cas d'interruption.
- Nommage automatique du fichier basé sur le titre de la vidéo.

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/gtentillier/video_downloader.git
cd video_downloader
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# ou
.\venv\Scripts\activate  # Sur Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Utilisation

### Tâche VS Code (Recommandé)
Le projet inclut une tâche VS Code pour automatiser tout le processus.
- Appuyez sur `Cmd+Shift+B` (ou `Ctrl+Shift+B`)
- Sélectionnez **"Full Download Process"**

Cette tâche va :
1. Récupérer le code source de la page définie dans [params.py](params.py).
2. Lancer le téléchargement avec `caffeinate` (pour empêcher l'ordinateur de s'endormir).

### Utilisation manuelle
Si vous préférez lancer les scripts séparément :

#### Étape 1 : Configurer l'URL
Modifiez `target_url` dans [params.py](params.py).

#### Étape 2 : Récupérer le code source
```bash
python fetch_source.py
```

#### Étape 3 : Télécharger la vidéo
```bash
python download_video.py
```

Le script lira `output.html`, extraira l'URL de la vidéo et lancera le téléchargement.

## Structure du projet

- [params.py](/Users/gaston/Code/projets/video_downloader/params.py) : Contient l'URL de la vidéo à télécharger.
- [fetch_source.py](/Users/gaston/Code/projets/video_downloader/fetch_source.py) : Récupère le HTML de la page cible.
- [download_video.py](/Users/gaston/Code/projets/video_downloader/download_video.py) : Analyse le HTML et télécharge le fichier MP4.
- `output.html` : Fichier temporaire contenant le code source (généré par `fetch_source.py`).

## Limitations

- Ce script est conçu spécifiquement pour la structure actuelle de TokyVideo.
- Les jetons de sécurité dans les URLs MP4 peuvent expirer après un certain temps. Si le téléchargement échoue avec une erreur 403, relancez `fetch_source.py` pour obtenir un nouveau lien.
