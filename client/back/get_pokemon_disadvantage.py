import requests
import logging


def get_pokemon_disadvantage(pk_selected: str, remove_prefix: bool):
    pk_selected = pk_selected.replace("%", "-")
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