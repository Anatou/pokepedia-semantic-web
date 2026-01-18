from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import get_pokemons
from get_pokemon_coverage import get_pokemon_coverage

# Lancer en étant dans le dossier server avec
# uvicorn app:app --port 8010
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Add the port your frontend is running on
    "http://localhost:5173",  # Vite's default port, add just in case
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/pokemons")
def read_pokemons(remove_prefix: bool = True):
    return get_pokemons.get_pokemons(remove_prefix)


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
