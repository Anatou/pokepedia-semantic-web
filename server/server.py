# rdflib & fastapi
from pathlib import Path
from rdflib import Graph

def to_string(s: str) -> str:
    permutations = {
        "-C2-A0": " ",
        "-C3-80": "À",
        "-C3-81": "Á",
        "-C3-82": "Â",
        "-C3-83": "Ã",
        "-C3-84": "Ä",
        "-C3-87": "Ç",
        "-C3-88": "È",
        "-C3-89": "É",
        "-C3-8A": "Ê",
        "-C3-8B": "Ë",
        "-C3-8E": "Î",
        "-C3-8F": "Ï",
        "-C3-94": "Ô",
        "-C3-99": "Ù",
        "-C3-A0": "à",
        "-C3-A2": "â",
        "-C3-A7": "ç",
        "-C3-A8": "è",
        "-C3-A9": "é",
        "-C3-AA": "ê",
        "-C3-AB": "ë",
        "-C3-AE": "î",
        "-C3-AF": "ï",
        "-C3-B3": "ó",
        "-C3-B4": "ô",
        "-C3-B9": "ù",
        "-C3-BB": "û",
    }
    s = s.replace("http://www.pokepedia.fr/Sp%C3%A9cial:URIResolver/", "")
    for word, permut in permutations.items():
        s = s.replace(word, permut)
    return s

# Guess the number of parts
N_PARTS = 1
while Path(f"data/pokepedia-fr_rdfdump20150715-part{N_PARTS}.rdf").exists():
    N_PARTS += 1
N_PARTS -= 1

data = ""
for part in range(N_PARTS):
    with open(f"data/pokepedia-fr_rdfdump20150715-part{part+1}.rdf", "r") as file:
        data += file.read()
g = Graph()
print("Reading RDF file...")
g.parse(data=data, format="application/rdf+xml")
print(len(g))

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

for r in g.query(q):
    types = r["type1"]
    if r["type2"]!=None:
        types += ' & '+r["type2"]
    print(f"{r.num}: {to_string(r.pk)}, type: {to_string(types)}, gen: {to_string(r.gen)}")