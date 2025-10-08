#!/bin/bash
set -e # Exit on any error

# Configuration
TIMEOUT=30

# Start container
echo "Starting container..."

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
docker rm -f "$NAME" || true
echo "✓ Smoke test passed"
