:: Start SPARQL endpoint
start cmd /k "cd server && python -m uvicorn app:app --port 8010"

:: Start backend
start cmd /k "cd client/back && python -m uvicorn app:app --port 8020"

:: Start frontend
start cmd /k "cd client/front && npm i && npm run dev"