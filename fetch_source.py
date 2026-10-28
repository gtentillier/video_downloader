import requests


def save_page_source(url, filename):
    try:
        # Envoi d'une requête GET
        response = requests.get(url, timeout=10)

        # Vérification si la requête a réussi (code 200)
        response.raise_for_status()

        # Enregistrement dans le fichier
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)

        return f"Succès : Le code source de {url} a été enregistré dans '{filename}'"
    except requests.exceptions.RequestException as err:
        return f"Erreur lors de la requête : {err}"
    except IOError as e:
        return f"Erreur lors de l'écriture du fichier : {e}"


if __name__ == "__main__":
    from params import target_url
    output_file = "output.html"

    result = save_page_source(target_url, output_file)
    print(result)
