# Setup and Configuration Guide

This guide provides comprehensive instructions for setting up and configuring Papercuts No More.

## Prerequisites

### Required Software
- **Docker Engine**: Version 20.10 or later
- **Docker Compose**: Version 2.0 or later
- Linux, macOS, or Windows (with WSL2)

### Optional Hardware/Software
- **Scanner Hardware**: Compatible scanner for document digitization
- **NVIDIA GPU**: For AI processing acceleration
  - NVIDIA drivers with CUDA support
  - Minimum 4GB VRAM recommended
- **Git**: Version control system

### System Requirements
- **Minimum**: 4GB RAM, 10GB free disk space
- **Recommended**: 8GB RAM, 50GB free disk space (for document storage)
- **GPU Mode**: Additional 2GB VRAM for AI acceleration

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/aliuosio/papercuts-nomore.git
cd papercuts-nomore
```

### 2. Choose Deployment Profile

#### Option A: NVIDIA GPU Acceleration (Recommended)
For systems with NVIDIA GPU and CUDA drivers:

```bash
docker compose --profile nvidia up -d
```

**Requirements**:
- NVIDIA GPU with CUDA 11.8+ support
- NVIDIA Container Toolkit installed
- Compatible NVIDIA drivers

#### Option B: CPU-Only Deployment
For systems without GPU or for compatibility:

```bash
docker compose up -d
```

### 3. Initial Startup

The first startup may take several minutes for:
- Downloading Docker images (~2-3GB)
- Auto-pulling Ollama qwen3:8b model (~4GB)
- Database initialization
- Service health checks

Monitor startup progress:
```bash
docker compose logs -f
```

## Service Access

After successful startup, access services at:

| Service | URL | Default Credentials |
|---------|-----|-------------------|
| Paperless-ngx | http://localhost:8010 | admin / admin123 |
| n8n Workflow Editor | http://localhost:5678 | - |
| Scanner Interface | http://localhost:8080 | - |
| Ollama API | http://localhost:11434 | - |

## Environment Configuration

### Environment Variables (.env)

The system uses comprehensive environment configuration. The `.env` file controls all service settings.

#### Database Configuration
```bash
# PostgreSQL
POSTGRES_DB=papercuts
POSTGRES_USER=papercuts
POSTGRES_PASSWORD=secure_password_here
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

#### Paperless-ngx Configuration
```bash
# Webserver settings
PAPERLESS_TIME_ZONE=Europe/Berlin
PAPERLESS_OCR_LANGUAGE=deu
PAPERLESS_CONSUMER_IGNORE_PATTERNS=*.log
PAPERLESS_FILENAME_FORMAT={created_year}/{created_month}/{title}

# Security
PAPERLESS_SECRET_KEY=your_secret_key_here
PAPERLESS_API_KEY=X3ooteih9th&ae9th0ahoh4ieH#
PAPERLESS_ADMIN_USER=admin
PAPERLESS_ADMIN_PASSWORD=admin123
```

#### AI Model Configuration
```bash
# Ollama settings
OLLAMA_MODEL=qwen3:8b
OLLAMA_KEEP_ALIVE=24h
OLLAMA_HOST=0.0.0.0:11434
```

#### Service Versions
```bash
# Service versions (pinned for stability)
PAPERLESS_VERSION=2.11.4
N8N_VERSION=1.60.1
OLLAMA_VERSION=0.3.12
POSTGRES_VERSION=16-alpine
REDIS_VERSION=7-alpine
```

### GPU-Specific Configuration

For NVIDIA GPU profile, additional configuration may be needed:

```bash
# GPU settings
NVIDIA_VISIBLE_DEVICES=all
NVIDIA_DRIVER_CAPABILITIES=compute,utility
CUDA_VISIBLE_DEVICES=0
```

## n8n Workflow Configuration

### Automatic Import
On first startup, n8n automatically imports pre-configured workflows located in `n8n_shared/`.

### Manual Workflow Setup

1. **Access n8n**: Open http://localhost:5678
2. **Import Workflows**:
   - Go to Settings → Import/Export
   - Upload workflow JSON files from `n8n_shared/`
3. **Configure AI Integration**:
   - Add Ollama Chat Model node
   - Set Base URL: `http://ollama-nvidia:11434` (GPU) or `http://ollama:11434` (CPU)
   - Select model: `qwen3:8b`

4. **Paperless API Integration**:
   - Add HTTP Request nodes
   - Set Base URL: `http://webserver:8000/api/` (internal)
   - Use Basic Authentication:
     - Username: `admin`
     - Password: `admin123`

## Scanner Integration

### Hardware Setup

1. **Connect Scanner**: Ensure scanner is properly connected and powered
2. **Verify Recognition**: Check scanner appears in system
   ```bash
   scanimage -L
   ```

### Scanservjs Configuration

Access the scanner interface at http://localhost:8080 and configure:

- **Device Selection**: Choose your scanner model
- **Scan Settings**:
  - Resolution: 300 DPI
  - Format: PDF (recommended) or TIFF
  - Color mode: Gray or Color
- **Output Directory**: Automatically set to shared volume

### Volume Integration

Scanned documents are automatically available in Paperless-ngx:

```bash
# Check shared volume
ls -la ./.docker/webserver/volumes/consume/
```

**Volume Mapping Details**:
- **Scanner Output**: `/var/lib/scanservjs/output` (container)
- **Paperless Input**: `./.docker/webserver/volumes/consume` (host)
- **Automatic Processing**: Files placed here are immediately processed

## Docker Compose Configuration

### Profile Management

#### Available Profiles
- **default**: CPU-only deployment
- **nvidia**: GPU-accelerated deployment

#### Switching Profiles
```bash
# Stop current deployment
docker compose down

# Switch to GPU mode
docker compose --profile nvidia up -d

# Or CPU mode
docker compose up -d
```

### Service Dependencies

```yaml
# docker-compose.yml key dependencies
services:
  db:
    # PostgreSQL - starts first
  redis:
    # Redis cache - starts second
  webserver:
    depends_on:
      - db
      - redis
  ollama:
    # AI service - starts independently
  n8n:
    depends_on:
      - webserver
      - ollama
  scanservjs:
    # Scanner service - independent
```

### Health Checks

All services include health checks:

```bash
# Check service health
docker compose ps
docker compose exec webserver curl -f http://localhost:8000/api/health/
```

## Volume Management

### Persistent Volumes

```
./.docker/
├── postgres/pgdata/_data/      # Database files
├── webserver/volumes/
│   ├── data/_data/            # Application data
│   ├── media/                 # Processed documents
│   └── consume/               # Incoming scans
└── n8n/                       # Workflow data
```

### Backup Strategy

**Critical Data to Backup**:
```bash
# Database backup
docker compose exec db pg_dump -U papercuts papercuts > backup.sql

# Document backup
cp -r ./.docker/webserver/volumes/ ./backups/

# AI Models (if needed)
cp -r ~/.ollama ./backups/
```

### Volume Permissions

Ensure proper permissions for shared volumes:

```bash
# Fix volume permissions if needed
sudo chown -R 1000:1000 ./.docker/webserver/volumes/
```

## Troubleshooting Setup

### Common Issues

#### 1. GPU Not Recognized
**Symptoms**: Services start but no GPU acceleration
**Check**:
```bash
nvidia-smi
docker run --gpus=all nvidia/cuda:11.8-base nvidia-smi
```
**Fix**: Install NVIDIA Container Toolkit

#### 2. Scanner Not Detected
**Symptoms**: Scanservjs shows no scanners
**Check**:
```bash
scanimage -L
lsusb  # For USB scanners
```
**Fix**: Verify scanner connection and permissions

#### 3. Port Conflicts
**Symptoms**: Services fail to start
**Check**:
```bash
netstat -tlnp | grep -E '(8010|5678|8080|11434)'
```
**Fix**: Change conflicting ports in docker-compose.yml

#### 4. Database Connection Issues
**Symptoms**: Paperless fails to start
**Check**:
```bash
docker compose logs db
docker compose exec db pg_isready -h localhost
```
**Fix**: Verify database credentials in .env

### Performance Optimization

#### GPU Mode Tuning
- Ensure adequate VRAM (minimum 4GB)
- Monitor GPU usage: `nvidia-smi`
- Adjust model size if needed

#### Memory Management
```bash
# Check container memory usage
docker stats
```

#### Disk Space Management
```bash
# Monitor storage usage
du -sh ./.docker/
df -h
```

## Upgrade Procedures

### Service Updates

1. **Stop services**:
   ```bash
   docker compose down
   ```

2. **Update images**:
   ```bash
   docker compose pull
   ```

3. **Update versions** in `.env` file if needed

4. **Restart services**:
   ```bash
   docker compose up -d
   ```

### Breaking Changes

- Always backup data before major version updates
- Review release notes for each service
- Test in development environment first

## Security Configuration

### Network Security
- Services communicate over secure Docker networks
- External access limited to necessary ports
- Database not directly exposed externally

### Authentication Security
- Change default admin password after first login
- Use strong passwords for all accounts
- Regularly update API keys

### Volume Security
- Ensure proper file permissions (typically 755)
- Avoid running containers as root where possible
- Regular security updates for base images

This setup guide should enable you to deploy and configure Papercuts No More successfully. Refer to the main README for quick start instructions, and see other documentation files for advanced topics.
