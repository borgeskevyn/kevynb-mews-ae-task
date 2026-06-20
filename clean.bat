@echo off
REM Stop and remove containers
docker rm -f fno_api_server pg_prod 2>NUL

REM Remove Docker network
docker network rm fno_net 2>NUL

REM Remove Docker image
docker rmi fno_api_server 2>NUL

REM Remove generated Dockerfile
del /f /q Dockerfile.api 2>NUL

REM Remove python virtual environment if it exists
if exist ".venv" (
    echo Removing Python virtual environment...
    rmdir /s /q .venv
)

echo Cleanup complete. All containers, images, network, and generated files removed.
