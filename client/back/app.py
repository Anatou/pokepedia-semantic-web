from fastapi import FastAPI, HTTPException
from get_pokemons import get_pokemons
from get_pokemon_coverage import get_pokemon_coverage

# Lancer en étant dans le dossier server avec
# uvicorn app:app --port 8010
app = FastAPI()


@app.get("/pokemons")
def exec_sparql(remove_prefix: bool = True):
    try:
        res = get_pokemons(remove_prefix)
        return res
    except BaseException as e:
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occured: {e}"
    )


@app.get("/pokemon/{pk}/coverage")
def exec_sparql(pk: str, remove_prefix: bool = True):
    try:
        res = get_pokemon_coverage(pk, remove_prefix)
        return res
    except BaseException as e:
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occured: {e}"
    )
