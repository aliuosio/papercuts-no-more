# Papercuts No More

A document digitization stack where **Scanservjs** captures documents → **Paperless-ngx** processes them with OCR and organizes in a database → **n8n** automates workflows for document processing → **Ollama** provides AI models for intelligent analysis and decision-making.

## Usage Guide

### Prerequisites

- Docker and Docker Compose installed
- Scanner hardware (optional, for scanning functionality)

### Setup

1. Clone this repository `git clone https://github.com/aliuosio/papercuts-nomore.git`
2. Startup
`docker compose --profile nvidia up -d (to use nvidia GPU)` or `docker compose (to use CPU)`
3. For custom API authentication: Ensure `.docker/custom-auth/` ownership is set to root:root

### Accessing Services

- **Paperless-ngx**: <http://localhost:8010> (default login: admin/admin123)
- **n8n**: <http://localhost:5678>
- **Scanner Interface**: <http://localhost:8080>
- **Ollama API**: <http://localhost:11434>

### Document Workflow

1. Scan documents using the scanner interface at port 8080
2. Documents are automatically consumed by Paperless-ngx
3. Use the web interface to organize, tag, and search documents
4. Create automated workflows in n8n to process documents (OCR, categorization, notifications, etc.)
5. Leverage Ollama for AI-powered document analysis and processing

### API Authentication

Paperless-ngx provides a REST API with custom X-API-Key authentication:

- **API Key**: Configured via `PAPERLESS_API_KEY` environment variable in `.env`
- **Change API Key**: Update the `PAPERLESS_API_KEY` value in `.env` and restart containers
- **Usage**: Include `X-API-Key: <your-api-key>` header in requests

Example API call:

    curl -H "X-API-Key: X3ooteih9th&ae9th0ahoh4ieH#" http://localhost:8010/api/documents/

**Note**: This uses custom authentication files in `.docker/custom-auth/` mounted at runtime, allowing use of the official Paperless-NGX image while maintaining API key functionality.

### Configuration

Environment variables are configured in the `.env` file:

- Database credentials
- Paperless-ngx settings (OCR language, timezone, etc.)
- Service versions and namespace

### Scanner Integration

Scanservjs saves scans to `/var/lib/scanservjs/output` in container (ephemeral without mapping). Paperless-ngx watches `./.docker/webserver/volumes/consume` (mapped to `/usr/src/paperless/consume`). Current mapping `./.docker/webserver/volumes/consume:/var/lib/scanservjs/output` enables automatic ingestion. Ensure write permissions; backups recommended as paperless processes/moves files. [Source](https://github.com/sbs20/scanservjs/blob/master/docs/02-docker.md#mapping-volumes).

## Architecture

- **Webserver (Paperless-ngx)**: Document management API and web interface on port 8010
- **n8n**: Workflow automation platform on port 5678
- **Ollama**: Local AI model server on port 11434 with configurable GPU support (Nvidia, AMD, CPU)
- **Database**: PostgreSQL for data storage
- **Broker**: Redis for caching and message queuing
- **Scanner**: Scanservjs for document scanning
