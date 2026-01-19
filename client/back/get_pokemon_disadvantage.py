import requests
import logging

permutations = {
    "-2D": "-", "-3A": ":", "-E2-99-82" : "F", "-E2-99-80" : "M", "-C5-93": "œ", "-C2-A0": " ", "-C3-80": "À", "-C3-81": "Á", "-C3-82": "Â", "-C3-83": "Ã", "-C3-84": "Ä", "-C3-87": "Ç", "-C3-88": "È", "-C3-89": "É", "-C3-8A": "Ê", "-C3-8B": "Ë", "-C3-8E": "Î", "-C3-8F": "Ï", "-C3-94": "Ô", "-C3-99": "Ù", "-C3-A0": "à", "-C3-A2": "â", "-C3-A7": "ç", "-C3-A8": "è", "-C3-A9": "é", "-C3-AA": "ê", "-C3-AB": "ë", "-C3-AE": "î", "-C3-AF": "ï", "-C3-B3": "ó", "-C3-B4": "ô", "-C3-B9": "ù", "-C3-BB": "û"
}


def get_pokemon_disadvantage(pk_selected: str, remove_prefix: bool):
    # on encode les caractères spéciaux dans la pk
    # on remplace les % dans la pk par des tirets pour match ce qui est dans la base
    for replacment, word in permutations.items():
        pk_selected = pk_selected.replace(word, replacment)
    query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX property: <http://www.pokepedia.fr/Sp%C3%A9cial:URIResolver/Attribut-3A> 
            PREFIX swivt: <http://semantic-mediawiki.org/swivt/1.0#>
            PREFIX wiki: <http://www.pokepedia.fr/Sp%C3%A9cial:URIResolver/>
            PREFIX category: <http://www.pokepedia.fr/Sp%C3%A9cial:URIResolver/Category-3A>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?pk
            WHERE {{
                ?pk wiki:avantage wiki:{pk_selected}.
            }}
    """
    try:
        res = requests.get(
                "http://localhost:8010/sparql",
                params={"query": query, "remove_prefix": remove_prefix},
                timeout=10
        )
        res.raise_for_status()
        formatted_res = {"coverage": res.json()}
        logging.info("Réponse reçue (%s)", res.status_code)
        logging.info("Contenu de la réponse: %s", res.text[:200] + "..." if len(res.text) > 200 else res.text)
        return formatted_res
    except requests.RequestException:
        logging.exception("Erreur lors de l'appel SPARQL")
        return {}
