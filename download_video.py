import argparse
import os
import re

import requests


def download_video(html_file, output_name=None):
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

    try:
        response = requests.get(video_url, headers=headers, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024 * 1024  # 1MB

        downloaded = 0
        with open(output_name, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                downloaded += len(data)
                if total_size:
                    done = int(50 * downloaded / total_size)
                    print(f"\r[{'=' * done}{' ' * (50-done)}] {downloaded/(1024*1024):.2f}MB / {total_size/(1024*1024):.2f}MB", end='')

        print(f"\n\nTéléchargement terminé : {os.path.abspath(output_name)}")

    except Exception as e:
        print(f"\nErreur lors du téléchargement : {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Télécharge une vidéo à partir d'un fichier HTML Tokyvideo.")
    parser.add_argument("file", help="Chemin vers le fichier HTML source")
    parser.add_argument("-o", "--output", help="Nom du fichier de sortie")

    args = parser.parse_args()
    download_video("/Users/gaston/SandBox/output.html")
