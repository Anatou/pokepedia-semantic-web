import requests
from json import loads as json_loads

q = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX property: <http://www.pokepedia.fr/Sp%C3%A9cial:URIResolver/Attribut-3A> 
PREFIX swivt: <http://semantic-mediawiki.org/swivt/1.0#>
PREFIX wiki: <http://www.pokepedia.fr/Sp%C3%A9cial:URIResolver/>
PREFIX category: <http://www.pokepedia.fr/Sp%C3%A9cial:URIResolver/Category-3A>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?num ?pk ?type1 ?type2 ?gen ?famille ?url 
WHERE { 
	?pk property:Num-C3-A9ro_National ?numString.
	?pk property:Premier_type ?type1.
	OPTIONAL { ?pk property:Second_type ?type2. }
	?pk rdfs:isDefinedBy ?url.
	?pk property:Famille ?famille.
	?pk property:G-C3-A9n-C3-A9ration_du_Pok-C3-A9mon ?gen
	BIND( xsd:integer(?numString) AS ?num)
	FILTER( ?num > 0 )
	FILTER( !regex(str(?pk), "Projet"))
	FILTER( !regex(str(?pk), "Utilisateur"))
}
ORDER BY asc(?num)
"""

res = requests.get("http://127.0.0.1:8000/sparql", params={"query": q, "remove_prefix": True})
for row in json_loads(res.text):
    print(row)