#!/bin/bash

# Function to restart Gunicorn
restart_gunicorn() {
    echo "Restarting Gunicorn..."
    pkill -f uvicorn
    uvicorn remanga_site.asgi:application &
}

# Start Gunicorn
uvicorn remanga_site.asgi:application &

# Watch for changes in the project directory and restart Gunicorn when necessary
while inotifywait -r -e modify,move,create,delete /home/deb/Python/pet_projects/manga_site_django; do 
    restart_gunicorn
done