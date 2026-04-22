# tests/integration.sh

#!/bin/bash

set -e

docker compose up -d

sleep 20

curl -X POST http://localhost:3000/job

sleep 10

curl http://localhost:3000/status

docker compose down