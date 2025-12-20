# Deployment Files

This directory contains all files needed for deploying the Model Server on a virtual machine.

## Quick Start

### Docker Deployment (Recommended - Easiest)

```bash
# Clone repository on your VM
git clone https://github.com/upskiller-xyz/server_template.git
cd server_template/deployment

# Run automated Docker deployment
sudo bash deploy-docker.sh
```

### Native Deployment (Traditional)

```bash
# Clone repository on your VM
git clone https://github.com/upskiller-xyz/server_template.git
cd server_template/deployment

# Run automated native deployment
sudo bash deploy.sh
```

## Files Included

### Docker Deployment Files

| File | Description |
|------|-------------|
| `deploy-docker.sh` | Automated Docker deployment script |
| `docker-compose.yml` | Docker Compose configuration |
| `.env.docker` | Docker environment configuration |
| `nginx-docker.conf` | Nginx configuration for Docker |
| `DOCKER_DEPLOYMENT.md` | Comprehensive Docker deployment guide |

### Native Deployment Files

| File | Description |
|------|-------------|
| `deploy.sh` | Automated native deployment script for VM setup |
| `stats.server.service` | Systemd service file for automatic startup |
| `nginx-stats.server.conf` | Nginx reverse proxy configuration |
| `.env.production` | Production environment configuration template |
| `VM_DEPLOYMENT.md` | Comprehensive native deployment documentation |

## Deployment Options

### Docker Deployment (Recommended)

**Pros**: Easiest setup, no Python version issues, consistent environment
**Cons**: Slight overhead, requires Docker

```bash
# Basic Docker deployment
sudo bash deploy-docker.sh

# With nginx reverse proxy
sudo bash deploy-docker.sh --with-nginx

# Custom port
sudo bash deploy-docker.sh --port 8082

# Force rebuild
sudo bash deploy-docker.sh --build

# Enable debug logging (for troubleshooting)
sudo bash deploy-docker.sh --debug
```

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for detailed documentation.

### Native Deployment

**Pros**: Native performance, minimal overhead
**Cons**: More complex setup, Python version dependencies

```bash
# Basic deployment
sudo bash deploy.sh --skip-nginx

# With nginx reverse proxy
sudo bash deploy.sh

# With custom domain and SSL
sudo bash deploy.sh --domain your-domain.com

# Custom port
sudo bash deploy.sh --port 8082

# Enable debug logging (for troubleshooting)
sudo bash deploy.sh --debug
```

See [VM_DEPLOYMENT.md](VM_DEPLOYMENT.md) for detailed documentation.

## Prerequisites

- Ubuntu 20.04+ or Debian 11+
- Python 3.11+
- Root/sudo access
- Minimum 2GB RAM

## File Locations After Deployment

| Item | Path |
|------|------|
| Application | `/opt/stats.server` |
| Virtual Environment | `/opt/stats.server/venv` |
| Configuration | `/opt/stats.server/.env` |
| Systemd Service | `/etc/systemd/system/stats.server.service` |
| Nginx Config | `/etc/nginx/sites-available/stats.server` |
| Application Logs | `/var/log/stats.server/` |
| Nginx Logs | `/var/log/nginx/stats.server-*.log` |

## Service Management

```bash
# Start/stop/restart service
sudo systemctl start stats.server
sudo systemctl stop stats.server
sudo systemctl restart stats.server

# View logs
sudo journalctl -u stats.server -f

# Check status
sudo systemctl status stats.server
```

## Testing Deployment

```bash
# Health check
curl http://localhost:8085/

# Expected response:
# {"status": "ready", "timestamp": "2025-01-01T00:00:00Z"}
```

## Debug Logging

Both deployment methods support debug mode for troubleshooting:

```bash
# Docker
sudo bash deploy-docker.sh --debug

# Native
sudo bash deploy.sh --debug
```

Debug mode provides:
- Verbose application logs
- Detailed request/response logging
- Stack traces for errors
- Performance timing information

See [DEBUG_LOGGING.md](DEBUG_LOGGING.md) for complete debug logging guide.

⚠ **Warning:** Debug mode is for troubleshooting only. Not recommended for production.

## Documentation

For detailed documentation, see:
- **[DEBUG_LOGGING.md](DEBUG_LOGGING.md)** - Debug logging guide
- **[DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)** - Docker deployment guide
- **[VM_DEPLOYMENT.md](VM_DEPLOYMENT.md)** - Native deployment guide
- **[../README.md](../README.md)** - Project overview and API documentation
- **[../docs/api.md](../docs/api.md)** - API reference

## Support

- Report issues: https://github.com/upskiller-xyz/server_template/issues
- Documentation: https://github.com/upskiller-xyz/server_template

## License

See [LICENSE](../docs/LICENSE) in the main repository.
