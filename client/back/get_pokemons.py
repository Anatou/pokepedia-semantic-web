from fastapi import FastAPI, HTTPException

# Lancer en étant dans le dossier server avec
# uvicorn app:app --port 8010

# Create FastAPI app instance
app = FastAPI()

# Define a simple GET endpoint
@app.get("/pokemons")
def exec_sparql():
    try:
        res = []
        
        return res
    except BaseException as e:
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occured: {e}"
        )
