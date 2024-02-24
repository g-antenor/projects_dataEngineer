docker compose ip init airflow

sleep 15

docker compose up -d

sleep 15

cd airbyte

if [ -f "docker-compose.yaml" ]; then
    docker compose up -d
else
    ./run-ab-platform.sh
fi