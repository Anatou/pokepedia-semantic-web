from pathlib import Path
from rdflib import Graph, Node
from rdflib.query import ResultRow

def fix_string_encoding(s: str, remove_prefix: bool) -> str:
    permutations = {
        "-C2-A0": " ", "-C3-80": "À", "-C3-81": "Á", "-C3-82": "Â", "-C3-83": "Ã", "-C3-84": "Ä", "-C3-87": "Ç", "-C3-88": "È", "-C3-89": "É", "-C3-8A": "Ê", "-C3-8B": "Ë", "-C3-8E": "Î", "-C3-8F": "Ï", "-C3-94": "Ô", "-C3-99": "Ù", "-C3-A0": "à", "-C3-A2": "â", "-C3-A7": "ç", "-C3-A8": "è", "-C3-A9": "é", "-C3-AA": "ê", "-C3-AB": "ë", "-C3-AE": "î", "-C3-AF": "ï", "-C3-B3": "ó", "-C3-B4": "ô", "-C3-B9": "ù", "-C3-BB": "û"
    }
    if remove_prefix: s = s.replace("http://www.pokepedia.fr/Sp%C3%A9cial:URIResolver/", "")
    for word, permut in permutations.items():
        s = s.replace(word, permut)
    return s

def fix_row_encoding(s: tuple[Node, Node, Node] | bool | ResultRow, remove_prefix: bool) -> str:
    if isinstance(s, ResultRow):
        res_dict = {}
        for key, value in s.asdict().items():
            res_dict[fix_string_encoding(key, remove_prefix)] = fix_string_encoding(value, remove_prefix)
        return res_dict
    elif isinstance(s, tuple):
        return (fix_string_encoding(s[0], remove_prefix), fix_string_encoding(s[1], remove_prefix), fix_string_encoding(s[2], remove_prefix))
    else:
        return s

def load_pokegraph() -> Graph:
    # Guess the number of parts
    FILE = "../data/pokepedia-fr_rdfdump20150715"
    N_PARTS = 1
    while Path(f"{FILE}-part{N_PARTS}.rdf").exists():
        N_PARTS += 1
    N_PARTS -= 1

    # Load the data
    print(f"Reading data from {N_PARTS} parts...", end="")
    data = ""
    for part in range(N_PARTS):
        with open(f"{FILE}-part{part+1}.rdf", "r") as file:
            data += file.read()
    # Parse the data
    print("Loading RDF graph...", end="\r")
    g = Graph()
    g.parse(data=data, format="application/rdf+xml")
    print(f"RDF graph ready with {len(g)} triplets !                                                                ")
    return g