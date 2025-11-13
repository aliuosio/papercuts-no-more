# Papercuts No More

A document digitization stack where **Scanservjs** captures documents → **Paperless-ngx** processes them with OCR and organizes in a database → **n8n** automates workflows for document processing → **Ollama** provides AI models for intelligent analysis and decision-making.

## Current Status

✅ **All services running and healthy**
- Paperless-ngx API: Fully operational with 65 documents
- Custom X-API-Key authentication: Active
- n8n workflows: Ready for automation
- Ollama AI models: Available for document analysis

## Usage Guide

### Prerequisites

- Docker and Docker Compose installed
- Scanner hardware (optional, for scanning functionality)

### Setup

1. Clone this repository `git clone https://github.com/aliuosio/papercuts-nomore.git`
2. Run `docker-compose up -d`
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

### Volumes

- `n8n_data`: n8n application data
- `redisdata`: Redis data persistence
- `./pgdata/_data`: PostgreSQL data
- `./data/_data`: Paperless-ngx data
- `./scans`: Scanned documents
- `./export`: Exported documents
- `~/Dokumente/Scans`: Host directory for document consumption

## Documentation

- **`codebase.md`**: Complete project overview and architecture documentation
- **`codebase-overview.md`** (in memory-bank): Authoritative source of truth for current system state
- **`endpoints.json`**: API endpoint definitions for n8n integration
- **`.docker/custom-auth/`**: Custom authentication setup for API key functionality

## Development Notes

- Custom API authentication requires `.docker/custom-auth/` files to be owned by root:root
- Memory-bank MCP stores project insights and current status
- All services use German language OCR configuration
- API supports both Token and X-API-Key authentication methods
