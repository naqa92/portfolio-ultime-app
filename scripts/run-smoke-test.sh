#!/bin/bash
set -e # Exit on any error

# Configuration
TIMEOUT=30

# Prepare database with migrations
echo "Preparing database for smoke test..."
rm -f instance/smoke_test.db # Clean up any existing test database
atlas migrate apply --env local --url "sqlite://instance/smoke_test.db"
echo "✓ Database migrations applied"

# Start container with volume mount for the database
echo "Starting container..."
docker run -d --rm --name "$NAME" \
  -p 5005:5000 \
  -v "$(pwd)/instance/smoke_test.db:/app/instance/todos.db:ro" \
  -e DATABASE_URL="sqlite:///instance/todos.db" \
  "$IMAGE"

# Wait for health check
echo "Waiting for container to be healthy..."
start=$(date +%s)

while true; do
	health=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$NAME" 2>/dev/null || echo "none")

	if [ "$health" = "healthy" ]; then
		echo "✓ Container is healthy"
		break
	fi

	now=$(date +%s)
	if [ $((now - start)) -ge $TIMEOUT ]; then
		echo "✗ Timeout waiting for container to become healthy"
		docker logs "$NAME" || true
		docker rm -f "$NAME" || true
		exit 1
	fi

	sleep 1
done

# Cleanup
echo "Cleaning up..."
docker rm -f "$NAME" || true
rm -f instance/smoke_test.db # Clean up test database
echo "✓ Smoke test passed"
