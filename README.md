# pokepedia-semantic-web

The project is splitted between client and sparql server
- The server exposes a SPARQL enpoint to which SPARQL requests can be made
- The client uses SPARQL requests to explore and present the data

# Requirements
This project uses **python 3.13.5** and **node 24.5.0** \
To install the depedencies, use `pip install -r requirements.txt` in the base directory

# SPARQL Server

### Start server
To launch the server, go in the `server/` directory and do `uvicorn app:app --port 8010`
```shell
cd server
uvicorn app:app --port 8010
```
### Utilization
The only endpoint is `http://localhost:8010/sparql` and has 2 GET parameters 
- `query`: (str) The SPARQL query to execute
- `remove_prefix`: (bool) Wether to remove the prefix before the names, ex: "http://prefix.example:Name" into "Name"

# Python Backend

TODO

# Vue.js Client

The frontend of this app is a Vue.js app.

Start it running in the `front/` directory:

```bash
npm i
npm run dev
```
