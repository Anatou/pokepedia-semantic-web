from fastapi import FastAPI, HTTPException
from sparql import fix_row_encoding, load_pokegraph

# Lancer en étant dans le dossier server avec
# uvicorn app:app --port 8010

# Create FastAPI app instance
app = FastAPI()
g = load_pokegraph()

# Define a simple GET endpoint
@app.get("/sparql")
def exec_sparql(query: str = "", remove_prefix: bool = False):
    if query == "":
        raise HTTPException(
            status_code=400,
            detail="Query string must not be empty"
        )
    
    try:
        res = []
        for r in g.query(query):
            res.append(fix_row_encoding(r, remove_prefix))
        return res
    except BaseException as e:
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occured: {e}"
        )