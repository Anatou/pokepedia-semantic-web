# python
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def get_pokemons(remove_prefix : bool):

    query = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?num ?pk ?type1 ?type2 ?gen ?famille ?url ?image
    WHERE { 
        ?pk property:Num-C3-A9ro_National ?numString.
        ?pk property:Premier_type ?type1.
        OPTIONAL { ?pk property:Second_type ?type2. }
        ?pk property:Famille ?famille.
        ?pk property:G-C3-A9n-C3-A9ration_du_Pok-C3-A9mon ?gen.

        # On construit l'URL Poképédia directement à partir de ?pk (qui est le nom)
        BIND(CONCAT("https://www.pokepedia.fr/", STR(?pk)) AS ?url)

        # On construit l'URL de l'image à partir du numéro national
        BIND(CONCAT("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/", ?numString, ".png") AS ?image)

        BIND(xsd:integer(?numString) AS ?num)
        FILTER( ?num > 0 )
        FILTER( !regex(str(?pk), "Projet"))
        FILTER( !regex(str(?pk), "Utilisateur"))
    }
    ORDER BY asc(?num)
    """

    #logging.info("Envoi de la requête SPARQL vers http://localhost:8010/sparql")
    try:
        res = requests.get(
            "http://localhost:8010/sparql",
            params={"query": query, "remove_prefix": remove_prefix},
            timeout=10
        )
        res.raise_for_status()
        formatted_res = {"pokemons": res.json()}
        #logging.info("Réponse reçue (%s)", res.status_code)
        #logging.info("Contenu de la réponse: %s", res.text[:200] + "..." if len(res.text) > 200 else res.text)
        return formatted_res
    except requests.RequestException:
        logging.exception("Erreur lors de l'appel SPARQL")
        return {}


