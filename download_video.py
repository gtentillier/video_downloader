import argparse
import os
import re

import requests
from tqdm import tqdm


def download_video(html_file='output.html', output_name=None):
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return

    # Recherche de l'URL source de la vidéo (MP4 avec jeton de sécurité)
    # Exemple: <source src="https://cdnst71.tokyvideo.com/videos/640/640135/mp4/..." type="video/mp4">
    match = re.search(r'<source src="(https?://[^"]+\.mp4\?[^"]+)"', content)

    if not match:
        print("URL de la vidéo non trouvée dans le code source.")
        return

    video_url = match.group(1)
    print(f"URL de la vidéo trouvée : {video_url}")

    if not output_name:
        # Essayer de trouver le titre de la vidéo
        title_match = re.search(r'data-title="([^"]+)"', content)
        if title_match:
            output_name = title_match.group(1).replace(' ', '_') + ".mp4"
        else:
            output_name = "video_tokyvideo.mp4"

    # Nettoyage du nom de fichier
    output_name = re.sub(r'[^\w\.-]', '_', output_name)

    print(f"Téléchargement vers : {output_name}...")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Referer': 'https://www.tokyvideo.com/'}

    # Gestion de la reprise du téléchargement
    file_mode = 'wb'
    initial_pos = 0
    if os.path.exists(output_name):
        initial_pos = os.path.getsize(output_name)
        # On ne reprend que si le fichier n'est pas vide
        if initial_pos > 0:
            headers['Range'] = f'bytes={initial_pos}-'
            file_mode = 'ab'
            print(f"Reprise du téléchargement à partir de {initial_pos} octets...")

    try:
        response = requests.get(video_url, headers=headers, stream=True)
        
        # Si on demande un Range et que le serveur ne le supporte pas (pas 206), on recommence à zéro
        if response.status_code == 416: # Range unsatisfiable
             print("Le fichier est probablement déjà complet.")
             return
        elif response.status_code != 206 and initial_pos > 0:
            print("Le serveur ne supporte pas la reprise. Redémarrage à zéro...")
            file_mode = 'wb'
            initial_pos = 0
            response = requests.get(video_url, headers={'User-Agent': headers['User-Agent'], 'Referer': headers['Referer']}, stream=True)

        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0)) + initial_pos
        block_size = 1024  # 1KB

        with open(output_name, file_mode) as f, tqdm(total=total_size, unit='iB', unit_scale=True, desc=output_name, leave=True, initial=initial_pos) as bar:
            for data in response.iter_content(block_size):
                size = f.write(data)
                bar.update(size)

        print(f"\n\nTéléchargement terminé : {os.path.abspath(output_name)}")

    except Exception as e:
        print(f"\nErreur lors du téléchargement : {e}")


if __name__ == "__main__":
    download_video()
