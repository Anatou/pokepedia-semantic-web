:: Start SPARQL endpoint
start cmd /k cd server && uvicorn app:app --port 8010

:: Start backend
start cmd /k cd client/back && uvicorn app:app --port 8020

:: Start frontend
start cmd /k cd client/front && npm i && npm run dev