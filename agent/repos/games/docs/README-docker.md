# Arcade Docker Run Instructions

To run the arcade app in a Docker container on a cluster with many agents:

1. Use the provided `arcade-docker-run.sh` script to automatically find an available port, run the container, and log the port for coordination.
2. The script will:
   - Search for an available port (starting at 3000)
   - Start the container with `-p <host_port>:3000` and `--env PORT=3000`
   - Overwrite `.arcade-ports` with the chosen port from the latest run
3. To stop a running container:
   - `docker ps` to find the container name (e.g., arcade-3001)
   - `docker stop <container_name>`
   - `docker rm <container_name>`

**Best Practices:**
- `.arcade-ports` reflects only the latest run and does not accumulate entries.
- Use `docker ps` to verify currently running containers if you need to cross-check stale state.
- If you need a specific port, you can run:
  `docker run -d -p 3002:3000 --env PORT=3000 --name arcade-3002 games`

**Note:** The app inside the container always listens on port 3000, but you can map any available host port to it.
