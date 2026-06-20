#!/bin/bash

# Stop and remove containers
docker rm -f fno_api_server pg_prod 2>/dev/null

# Remove Docker network
docker network rm fno_net 2>/dev/null

# Remove Docker image
docker rmi fno_api_server 2>/dev/null

# Remove generated Dockerfile
rm -f Dockerfile.api

# Remove python virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Removing Python virtual environment..."
    rm -rf .venv
fi

echo "Cleanup complete. All containers, images, network, and generated files removed."
