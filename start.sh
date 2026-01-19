if [ "$OSTYPE" == "linux-gnu" ]; then
    case "$TERMINAL" in
        kitty)
            # Start SPARQL endpoint
            kitty --detach sh -c "cd server && uvicorn app:app --port 8010"
            # Start backend
            kitty --detach sh -c "cd client/back && uvicorn app:app --port 8020"
            # Start frontend
            kitty --detach sh -c "cd client/front && npm i && npm run dev";;
        *) echo "Script not configured to open this terminal emulator"
    esac 
elif [ "$OSTYPE" == "darwin"* ]; then
    osascript -e 'tell app "Terminal" to do script "cd server && uvicorn app:app --port 8010"'
    osascript -e 'tell app "Terminal" to do script "cd client/back && uvicorn app:app --port 8020"'
    osascript -e 'tell app "Terminal" to do script "cd client/front && npm i && npm run dev"'
fi