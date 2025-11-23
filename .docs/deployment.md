# Deployment and Development Guide

This guide covers deployment strategies, development workflows, and operational considerations for Papercuts No More.

## Deployment Options

### Production Deployment

#### Prerequisites
- Production-grade server (minimum 8GB RAM, 100GB SSD)
- Domain name with SSL certificate
- Backup solution (automated)
- Monitoring and alerting system

#### Security Hardening

**Network Security**:
```yaml
# docker-compose.prod.yml
services:
  webserver:
    environment:
      - PAPERLESS_CORS_ALLOWED_HOSTS=https://yourdomain.com
      - PAPERLESS_FORCE_SCRIPT_NAME=/paperless
    networks:
      - proxy  # For reverse proxy
      - internal
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.paperless.rule=Host(`paperless.yourdomain.com`)"
      - "traefik.http.routers.paperless.tls.certresolver=letsencrypt"
```

**SSL/TLS Configuration**:
- Use reverse proxy (Traefik, nginx, Caddy)
- Enable HTTP to HTTPS redirects
- Configure proper SSL certificates

**Environment Security**:
- Use Docker secrets for sensitive data
- Rotate API keys regularly
- Disable debug mode in production

### Cloud Deployment

#### AWS EC2
```bash
# Instance requirements
# t3.medium or larger (2 vCPU, 4GB RAM minimum)
# Ubuntu 22.04 LTS with NVIDIA drivers (for GPU)

# Security group rules
# SSH (22) - restrict to your IP
# HTTP (80) - for Let's Encrypt challenges
# HTTPS (443) - main access
# Custom ports for services (8010, 5678, etc.) - restrict to local/VPC
```

#### Docker Swarm/Kubernetes

**Docker Swarm**:
```yaml
version: '3.8'
services:
  papercuts:
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
    secrets:
      - postgres_password
      - paperless_secret_key
      - paperless_api_key
```

### Development Environment

#### Local Development Setup

1. **Clone and setup**:
```bash
git clone https://github.com/aliuosio/papercuts-nomore.git
cd papercuts-nomore
cp .env.example .env  # Configure environment variables
```

2. **Development overrides**:
```yaml
# docker-compose.dev.yml
services:
  webserver:
    environment:
      - PAPERLESS_DEBUG=true
      - PAPERLESS_DISABLE_LOGIN=true  # For easier development
    volumes:
      - ./src:/usr/src/paperless/src  # Mount source code
  n8n:
    environment:
      - N8N_LOG_LEVEL=debug
```

3. **Start development environment**:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

## Environment Management

### Environment Files

**Structure your `.env` files**:

```bash
# .env
# Common settings
COMPOSE_PROJECT_NAME=papercuts
TZ=Europe/Berlin

# Database
POSTGRES_DB=papercuts
POSTGRES_USER=papercuts
POSTGRES_PASSWORD=
POSTGRES_HOST=db

# Paperless
PAPERLESS_SECRET_KEY=
PAPERLESS_TIME_ZONE=Europe/Berlin
PAPERLESS_OCR_LANGUAGE=deu
PAPERLESS_ADMIN_USER=admin
PAPERLESS_ADMIN_PASSWORD=

# Development overrides in .env.dev
# .env.dev
PAPERLESS_DEBUG=true
N8N_LOG_LEVEL=debug
```

### Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `POSTGRES_DB` | Database name | papercuts | Yes |
| `PAPERLESS_SECRET_KEY` | Django secret key | - | Yes |
| `PAPERLESS_TIME_ZONE` | System timezone | Europe/Berlin | No |
| `OLLAMA_MODEL` | AI model name | qwen3:8b | No |
| `PAPERLESS_OCR_LANGUAGE` | OCR languages | deu | No |
| `N8N_LOG_LEVEL` | Logging verbosity | info | No |

## Development Workflow

### Code Development

**Modifying Paperless-ngx**:
```bash
# Enter container
docker compose exec webserver bash

# Make changes to source code
cd /usr/src/paperless
vim paperless/settings.py

# Restart service
docker compose restart webserver
```

**n8n Workflow Development**:
1. Access http://localhost:5678
2. Enable developer mode for advanced features
3. Use built-in testing tools
4. Export/import workflows via JSON

### Testing Strategy

#### Unit Tests
```bash
# Run Paperless tests
docker compose exec webserver python manage.py test

# Run Ollama model validation
curl http://localhost:11434/api/tags
```

#### Integration Tests
```bash
# Test API connectivity
curl -u admin:admin123 http://localhost:8010/api/documents/

# Test scanner integration
curl http://localhost:8080/scanner/status
```

#### End-to-End Testing
- Manual testing of document workflows
- Scanner hardware testing
- AI chat interface validation
- Performance testing with large document sets

### Debugging Techniques

#### Container Logs
```bash
# Follow all service logs
docker compose logs -f

# Specific service logs
docker compose logs -f webserver

# Filter logs by time
docker compose logs --since "1h" webserver
```

#### Database Debugging
```bash
# Access PostgreSQL
docker compose exec db psql -U papercuts -d papercuts

# Common queries
SELECT COUNT(*) FROM documents_document;
SELECT * FROM documents_tag LIMIT 5;
```

#### Performance Monitoring
```bash
# Container resource usage
docker stats

# Disk usage
du -sh ./.docker/webserver/volumes/

# Network connections
netstat -tlnp | grep -E '(8010|5678|8080|11434)'
```

## Backup and Recovery

### Automated Backups

**Database Backup Script**:
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Database backup
docker compose exec -T db pg_dump -U papercuts papercuts > "$BACKUP_DIR/database.sql"

# Document backup
cp -r ./.docker/webserver/volumes/media "$BACKUP_DIR/"
cp -r ./.docker/webserver/volumes/data "$BACKUP_DIR/"

# Compress backup
tar -czf "$BACKUP_DIR.tar.gz" -C "$BACKUP_DIR" .
rm -rf "$BACKUP_DIR"

echo "Backup completed: $BACKUP_DIR.tar.gz"
```

**Automated Backups with Cron**:
```bash
# Add to crontab (crontab -e)
0 2 * * * /path/to/papercuts/backup.sh  # Daily at 2 AM
```

### Recovery Procedures

**Database Restore**:
```bash
# Stop services
docker compose down

# Restore database
docker compose exec -T db psql -U papercuts -d papercuts < backup.sql

# Restart services
docker compose up -d
```

**Full System Restore**:
```bash
# Extract backup
tar -xzf backup.tar.gz
cd backup

# Restore volumes
cp -r data/* ../.docker/webserver/volumes/data/
cp -r media/* ../.docker/webserver/volumes/media/
```

### Disaster Recovery Planning

1. **Offsite Backups**: Sync backups to cloud storage (AWS S3, Google Cloud)
2. **Backup Testing**: Regularly test restore procedures
3. **Retention Policy**: Keep backups for 30 days minimum
4. **Emergency Access**: Document procedures for quick recovery

## Monitoring and Observability

### Health Checks

**Service Health Endpoints**:
```bash
# Paperless health
curl http://localhost:8010/api/health/

# Ollama health
curl http://localhost:11434/api/tags

# n8n health
curl http://localhost:5678/healthz
```

### Metrics Collection

**Basic Monitoring Script**:
```bash
#!/bin/bash
# monitor.sh
echo "=== Papercuts No More Status ==="
echo "Date: $(date)"

# Service status
docker compose ps --format "table {{.Name}}\t{{.Status}}"

# Disk usage
echo -e "\nDisk Usage:"
du -sh ./.docker/webserver/volumes/ ~/.ollama/

# Document count
echo -e "\nDocument Statistics:"
curl -s -u admin:admin123 http://localhost:8010/api/documents/ | jq .count 2>/dev/null || echo "Unable to fetch document count"
```

### Alerting Setup

**Basic Alerts**:
- Service down notifications (email, Slack)
- Disk space warnings
- Failed backup alerts
- High CPU/memory usage

## Optimization Strategies

### Performance Tuning

#### Database Optimization
```sql
-- Create indexes for common queries
CREATE INDEX CONCURRENTLY idx_documents_created ON documents_document (created);
CREATE INDEX CONCURRENTLY idx_documents_content ON documents_document USING gin (content);

-- Analyze table statistics
ANALYZE VERBOSE documents_document;
```

#### Memory Optimization
```yaml
# docker-compose.yml memory limits
services:
  webserver:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
  n8n:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

#### Cache Optimization
- Redis for session storage and query caching
- Browser caching for static assets
- CDN for frequently accessed files

### Scaling Considerations

#### Horizontal Scaling
- Database read replicas for performance
- Load balancer for multiple web server instances
- Distributed file storage for large document collections

#### Vertical Scaling
- Increase CPU cores for better OCR performance
- Add more RAM for larger model processing
- GPU upgrades for AI acceleration

## Troubleshooting

### Common Issues

#### Service Startup Failures

**PostgreSQL won't start**:
- Check disk space: `df -h`
- Verify volume permissions
- Check PostgreSQL logs: `docker compose logs db`

**Paperless fails to initialize**:
- Verify database connectivity
- Check environment variables
- Review migration logs

#### Performance Issues

**Slow OCR processing**:
- Optimize image resolution
- Enable GPU acceleration
- Adjust worker threads

**High memory usage**:
- Monitor with `docker stats`
- Implement memory limits
- Optimize image cleanup

#### Connectivity Issues

**Internal service communication**:
- Verify Docker networks
- Check service names in docker-compose.yml
- Test connectivity with `docker compose exec`

### Log Analysis

**Log Locations**:
```bash
# Service logs
docker compose logs webserver
docker compose logs n8n
docker compose logs db

# System logs
journalctl -u docker

# Application logs inside containers
docker compose exec webserver tail -f /usr/src/paperless/data/logs/paperless.log
```

## Contributing

### Development Environment Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/papercuts-nomore.git
cd papercuts-nomore

# Set up pre-commit hooks
pip install pre-commit
pre-commit install

# Start development environment
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### Code Quality

```bash
# Run linting
docker compose exec webserver python -m flake8 .

# Run tests
docker compose exec webserver python manage.py test

# Format code
docker compose exec webserver python -m black .
```

### Pull Request Process

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes with tests
3. Update documentation
4. Create pull request with detailed description
5. Wait for review and approval

## Version Management

### Semantic Versioning

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, no new features

### Release Process

1. Update version in `.env` and docker-compose.yml
2. Create release branch: `git checkout -b release/v1.2.3`
3. Tag release: `git tag v1.2.3`
4. Create GitHub release with changelog
5. Merge to main and deploy

### Docker Image Tagging

```yaml
# docker-compose.yml
services:
  webserver:
    image: ghcr.io/papermless-ngx/paperless-ngx:2.11.4  # Specific version
    # or
    image: ghcr.io/papermless-ngx/paperless-ngx:latest  # Latest (not recommended for production)
```

## Support and Community

### Getting Help

1. **Documentation**: Check docs/ directory first
2. **GitHub Issues**: Search existing issues
3. **Community Forums**: Paperless-ngx discourse
4. **Logs**: Provide relevant log excerpts

### Support Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community support
- **Paperless-ngx Forums**: Upstream component support
- **n8n Community**: Workflow automation help

This deployment guide provides comprehensive information for operating Papercuts No More in various environments, from local development to production deployment with proper monitoring, backup, and scaling strategies.
