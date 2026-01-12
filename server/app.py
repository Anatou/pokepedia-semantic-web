from fastapi import FastAPI
from sparql import fix_row_encoding, load_pokegraph

# uvicorn app:app --reload
# Create FastAPI app instance
app = FastAPI()
g = load_pokegraph()

# Define a simple GET endpoint
@app.get("/sparql")
def exec_sparql(query: str = "", remove_prefix: bool = False):
    if query == "":
        return ["Empty query"]
    
    try:
        res = []
        for r in g.query(query):
            res.append(fix_row_encoding(r, remove_prefix))
        return res
    except BaseException as e:
        return [f"An internal error occured: {e}"]