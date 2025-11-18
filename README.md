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

### Pre-configured n8n Workflow

On docker-compose startup, a workflow is automatically imported into n8n. This includes a chat interface that uses Ollama's AI model to communicate with the paperless-ngx API, enabling natural language queries of your document database.

**Example query:** "What documents were added in October about insurance?"

The chat analyzes your questions and queries the paperless-ngx API to retrieve relevant documents based on content, metadata, dates, and tags.

#### Ollama Chat Model Configuration

The n8n workflow includes an Ollama Chat Model node that powers the AI assistant. Configure it as follows:

**Base URL Configuration:**
- When using NVIDIA GPU profile (`docker compose --profile nvidia up -d`): Set the Base URL to `http://ollama-nvidia:11434`
- When using CPU profile (`docker compose up -d`): Set the Base URL to `http://ollama:11434`

**Model Selection:**
The docker-compose.yml automatically pulls the `qwen3:8b` model. In the Ollama Chat Model node within n8n:
1. Open the workflow editor
2. Select the Ollama Chat Model node (likely named "Ollama" or similar)
3. Ensure the Base URL is set as above depending on your profile
4. Select `qwen3:8b` from the model dropdown menu

### API Authentication

Paperless-ngx provides a REST API with custom X-API-Key authentication:

- **API Key**: Configured via `PAPERLESS_API_KEY` environment variable in `.env`
- **Change API Key**: Update the `PAPERLESS_API_KEY` value in `.env` and restart containers
- **Usage**: Include `X-API-Key: <your-api-key>` header in requests

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
