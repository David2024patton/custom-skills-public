---
name: docker-ops
description: Docker container management, compose operations, health checks, and troubleshooting. Use when working with Docker containers, deploying services, debugging container issues, or managing volumes.
---
> [!IMPORTANT]
> **Core Directives Apply** (inlined here in full; there is no separate core-directives skill to load): Always be cutting-edge (latest stable versions, modern patterns). Always be modular (single-responsibility, composable, testable in isolation). Always think outside the box (question assumptions, cross-pollinate techniques, find the 10-line solution). These three directives are the complete engineering philosophy this skill relies on: prefer the latest stable version and modern pattern over a legacy approach, keep every unit single-responsibility and independently testable, and question assumptions to find the simpler cross-pollinated solution before settling.


# Docker Operations

Ported from iTaK `skills/docker_ops.md` and enriched with David's infrastructure patterns.

## Installing Docker

### Check if Docker is Installed

```bash
docker --version
docker compose version
```

If both commands return version numbers, Docker is ready. Otherwise, install it below.

### Windows

```powershell
# Option 1: Docker Desktop (recommended for development)
winget install Docker.DockerDesktop

# After install, restart your terminal. Docker Desktop must be running.
# Enable WSL 2 backend in Docker Desktop Settings > General
```

Or download manually from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)

### macOS

```bash
# Via Homebrew
brew install --cask docker

# Launch Docker.app from Applications, then verify:
docker --version
```

### Linux (Ubuntu/Debian)

```bash
# Remove old versions
sudo apt-get remove docker docker-engine docker.io containerd runc 2>/dev/null

# Install via official script (fastest)
curl -fsSL https://get.docker.com | sudo sh

# Add current user to docker group (avoids needing sudo)
sudo usermod -aG docker $USER
newgrp docker

# Enable on boot
sudo systemctl enable docker
sudo systemctl start docker

# Verify
docker run hello-world
```

### Post-Install Verification

```bash
docker --version           # Should show Docker version 24+
docker compose version     # Should show Compose v2+
docker run hello-world     # Should pull and run successfully
```

## Container Lifecycle

### Start services

```bash
docker compose up -d              # All services
docker compose up -d neo4j        # Single service
docker compose up -d --build      # Rebuild and start
```

### Stop services

```bash
docker compose down               # Stop all
docker compose down -v            # Stop and remove volumes (data loss!)
docker compose stop neo4j         # Stop single service
```

### Check status

```bash
docker compose ps                 # All containers
docker compose logs -f            # Follow all logs
docker compose logs -f itak       # Follow specific service
docker compose logs --tail=50     # Last 50 lines
```

### Debug a container

```bash
docker exec -it <container> bash          # Shell into running container
docker inspect <container>                # Full container details
docker stats                              # Resource usage
docker compose config                     # Validate compose file
```

## Common Operations

### Restart a crashed service

```bash
docker compose restart neo4j
```

### Update a service without downtime

```bash
docker compose pull neo4j                # Pull latest image
docker compose up -d --no-deps neo4j     # Restart just that service
```

### Clean up

```bash
docker system prune -f                   # Remove unused containers/images
docker volume prune -f                   # Remove unused volumes
docker image prune -a -f                 # Remove all unused images
```

### Backup volumes

```powershell
# PowerShell
docker run --rm -v neo4j-data:/data -v "${PWD}:/backup" alpine tar czf /backup/neo4j-backup.tar.gz /data
```

```bash
# Linux/SSH
docker run --rm -v neo4j-data:/data -v $(pwd):/backup alpine tar czf /backup/neo4j-backup.tar.gz /data
```

## iTaK Ecosystem Port Mapping

| Service | Container Port | Host Port |
| --- | --- | --- |
| Neo4j HTTP | 7474 | 47474 |
| Neo4j Bolt | 7687 | 47687 |
| Weaviate | 8080 | 48080 |
| SearXNG | 8080 | 48888 |
| WebUI | 8920 | 48920 |

> **Rule**: Always use obfuscated 5-digit ports for new services.

## Health Checks

### Neo4j

```bash
curl -s http://localhost:47474 | head -1
```

### Weaviate

```bash
curl -s http://localhost:48080/v1/.well-known/ready
```

| Neo4j HTTP | 7474 | 47474 |
| Neo4j Bolt | 7687 | 47687 |
| Weaviate | 8080 | 48080 |
| SearXNG | 8080 | 48888 |
| WebUI | 8920 | 48920 |

> **Rule**: Always use obfuscated 5-digit ports for new services.

## Health Checks

### Neo4j

```bash
curl -s http://localhost:47474 | head -1
```

### Weaviate

```bash
curl -s http://localhost:48080/v1/.well-known/ready
```

### SearXNG

```bash
curl -s http://localhost:48888/healthz
```

## VPS Operations

```bash
# SSH to VPS
ssh root@<vps-ip>

# Check all running containers on VPS
ssh root@<vps-ip> "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

# View logs remotely
ssh root@<vps-ip> "docker compose -f /path/to/docker-compose.yml logs --tail=50"
```

## Troubleshooting

| Issue | Fix |
| --- | --- |
| Port already in use | `docker compose down` then `docker compose up -d` |
| Volume permission denied | `chmod -R 777 ./data` or recreate volumes |
| Container keeps restarting | Check logs: `docker compose logs <service>` |
| Out of disk space | `docker system prune -a -f` |
| Network issues between services | Ensure all on same network |
| Neo4j 15-min lockout | Wait 15 minutes or restart the container |
| Neo4j credential reset | Stop container, delete volume, restart (first-boot restriction) |

## Verifying an image's contents when the Docker daemon will NOT start

On the Windows host, Docker Desktop sometimes never brings the engine up: `docker desktop status` stays `starting`, the `//./pipe/dockerDesktopLinuxEngine` pipe never appears, and `%LOCALAPPDATA%\Docker\log\host\com.docker.backend.exe.log` repeats `docker daemon still not ready ... context deadline exceeded`. Relaunching twice does not fix it. Do not block on it, and never report a build you did not run.

Verify at the registry instead (script pattern used 2026-10-24, saved with that task as `verify_image.py`):

1. Token: `https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/<name>:pull`.
2. HEAD `https://registry-1.docker.io/v2/library/<name>/manifests/<tag>` with the OCI index + manifest accept headers: `Docker-Content-Digest` is the index digest for a `FROM image:tag@sha256:...` pin.
3. Pick `linux/amd64` from the index, GET that manifest, then GET the config blob: `GOLANG_VERSION` in `Env` proves a builder tag's Go version without pulling it.
4. Download each layer blob and read `lib/apk/db/installed` from the tar (last layer carrying it wins): `P:<pkg>` / `V:<version>` records give exact package versions (e.g. `libssl3 = 3.5.9-r0` vs `3.3.3-r0`), which is how an OpenSSL CVE fix is proven without running anything.

Note: `golang:<ver>-alpine` images also carry `GOTOOLCHAIN=local` in `Env`, which is what makes the go.mod `toolchain` line useless inside those builds (see the golang skill).

## PowerShell Equivalents (Windows)

```powershell
# List containers
docker ps -a

# Container logs
docker logs -f CONTAINER

# Compose up/down
docker compose up -d
docker compose down
```
