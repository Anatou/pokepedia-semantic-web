# Start SPARQL endpoint
$TERMINAL --detach sh -c "cd server && uvicorn app:app --port 8010"

# Start backend
$TERMINAL --detach sh -c "cd client/back && uvicorn app:app --port 8020"

# Start frontend
$TERMINAL --detach sh -c "cd client/front && npm i && npm run dev"