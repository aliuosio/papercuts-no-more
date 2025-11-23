# Papercuts No More

A comprehensive document digitization and management system that combines scanning, OCR processing, AI-powered analysis, and workflow automation. This stack transforms physical documents into an intelligent, searchable database with natural language querying capabilities.

## Architecture Overview

The system consists of multiple interconnected services running in Docker containers:

### Core Services

- **Webserver (Paperless-ngx)**: Document management API and web interface on port 8010
  - Document ingestion, OCR processing, and storage
  - REST API with authentication support
  - Supports multiple file formats and automatic categorization

- **n8n**: Workflow automation platform on port 5678
  - Provides intelligent chat interface for document queries
  - AI-powered agent using Ollama for natural language processing
  - Automated workflow execution and API integration

- **Ollama**: Local AI model server on port 11434 with configurable GPU support (Nvidia, AMD, CPU)
  - Runs qwen3:8b model for document analysis and chat
  - Configurable for both NVIDIA GPU and CPU-only environments
  - Persistent model storage at ~/.ollama

- **Database**: PostgreSQL for data storage
  - Persistent data storage for documents, metadata, and relationships
  - Configured with German localization (deu)

- **Broker**: Redis for caching and message queuing
  - Provides caching layer and message passing between services

- **Scanner**: Scanservjs for document scanning
  - Web-based scanner interface on port 8080
  - Automatically integrates with Paperless-ngx for document ingestion

## Usage Guide

### Prerequisites

- Docker and Docker Compose installed
- Scanner hardware (optional, for scanning functionality)
- NVIDIA GPU with CUDA drivers (optional, for GPU acceleration)

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/aliuosio/papercuts-nomore.git
   cd papercuts-nomore
   ```

2. Choose your deployment mode:

   **For NVIDIA GPU acceleration:**
   ```bash
   docker compose --profile nvidia up -d
   ```

   **For CPU-only processing:**
   ```bash
   docker compose up -d
   ```

### Accessing Services

- **Paperless-ngx**: <http://localhost:8010> (default login: admin/admin123)
- **n8n Workflow Editor**: <http://localhost:5678>
- **Scanner Interface**: <http://localhost:8080>
- **Ollama API**: <http://localhost:11434>

### GPU Configuration

The system supports NVIDIA GPU acceleration for AI processing:

- **GPU Requirements**: NVIDIA GPU with compatible CUDA drivers on host system
- **Profiles**:
  - `nvidia` profile: Enables GPU acceleration for Ollama with optimized performance
  - `cpu` profile: CPU-only execution for broader compatibility
- **Performance Benefits**: Up to 500% faster AI processing with GPU acceleration
- **Automatic Model Loading**: qwen3:8b model is automatically pulled and optimized for your hardware

### Document Workflow

1. **Scan**: Use Scanservjs interface (port 8080) to scan documents
2. **Auto-Ingest**: Scanned files automatically appear in Paperless-ngx consume directory
3. **Processing**: Paperless-ngx performs OCR and categorization
4. **AI Chat**: Query documents using n8n chat interface (port 5678)
5. **Management**: Organize, tag, and search documents via web interface (port 8010)

## AI-Powered Document Intelligence

### Pre-configured n8n Workflow

On startup, a comprehensive workflow is automatically imported into n8n featuring:

- **Natural Language Chat Interface**: Communicate with your document database using natural language
- **Ollama Integration**: AI model provides intelligent query understanding and document retrieval
- **Multi-criteria Search**: Based on content, metadata, dates, and tags

**Example queries:**
- "What documents were added in October about insurance?"
- "Show me contracts signed in 2023"
- "Find all receipts from Amazon this month"
- "Get tax documents from 2022"

### Ollama AI Integration

- **Model**: Automatically pulls and serves qwen3:8b on startup
- **Service Names**:
  - `ollama-nvidia` for GPU profile (connects to http://ollama-nvidia:11434)
  - `ollama` for CPU profile (connects to http://ollama:11434)
- **n8n Configuration**: Ollama Chat Model node configured for AI agent functionality
- **Keep Alive**: 24-hour model retention to reduce reload times

### n8n Workflow Configuration

**Base URL Configuration:**
- GPU profile: Set Ollama Chat Model Base URL to `http://ollama-nvidia:11434`
- CPU profile: Set Ollama Chat Model Base URL to `http://ollama:11434`

**Model Selection:**
1. Open n8n workflow editor at http://localhost:5678
2. Select the Ollama Chat Model node
3. Select `qwen3:8b` from the model dropdown menu

## API Authentication

Paperless-ngx provides a REST API with multiple authentication methods:

### Current Working Authentication Methods

**Basic Authentication (Recommended):**
- **Username**: `admin`
- **Password**: `admin123`
- **Usage**: Use HTTP Basic Auth in your API requests
- **From n8n/internal**: `http://webserver:8000/api/`
- **External access**: `http://localhost:8010/api/`

**Token Authentication:**
- Obtain token via POST to `/api/token/` with credentials
- Use `Authorization: Token <token>` header in subsequent requests

### Custom X-API-Key Authentication (Future)

*Note: Custom X-API-Key authentication is planned but currently not active. The system requires custom authentication scripts to enable this feature.*

- **Planned Implementation**: Create `/.docker/custom-auth/` directory with authentication scripts
- **Expected Usage**: `X-API-Key: <your-api-key>` header
- **Current Status**: Falls back to standard token-based authentication

### API Key Configuration

- Environment variable: `PAPERLESS_API_KEY` in `.env`
- To change key: Update `.env` and restart containers

## Comprehensive Configuration

### Environment Variables (.env)

The system uses comprehensive environment configuration:

- **Database**: PostgreSQL credentials and connection settings
- **Paperless-ngx**: OCR language (German: deu), timezone (Europe/Berlin), UI settings
- **Service Versions**: Specific versions for all services
- **Security**: API keys, passwords, namespace isolation
- **GPU Settings**: NVIDIA GPU configuration and CUDA parameters
- **AI Model**: Ollama model selection and keep-alive settings

### Service Configuration

#### Ports Mapping
- Scanservjs: 8080
- Paperless-ngx: 8010 → 8000 (internal)
- n8n: 5678 → 5678
- Ollama: 11434 → 11434
- PostgreSQL: 5432 (exposed for debugging)

#### Volume Management
- **Database**: `./.docker/postgres/pgdata/_data`
- **Paperless Data**: `./.docker/webserver/volumes/data/_data`
- **Paperless Media**: `./.docker/webserver/volumes/media`
- **Paperless Consume**: `./.docker/webserver/volumes/consume`
- **n8n Data**: Docker volume `n8n_data`
- **Ollama Models**: `~/.ollama` (host directory)

### Scanner Integration

Scanservjs automatically integrates with Paperless-ngx:

- **Scan Output**: `/var/lib/scanservjs/output` (container)
- **Paperless Watch**: `./.docker/webserver/volumes/consume`
- **Auto-Ingest**: Mapped volume enables automatic document processing
- **Backup Recommendation**: Regular backups of consume directory recommended

## Security Features

- **Containerized Isolation**: All services run in separate containers
- **Authentication**: Multiple authentication methods for API access
- **Network Security**: Internal networking between services
- **Custom Authentication**: Support for custom auth scripts
- **PostgreSQL Collation**: Fixes for international character handling

## Development and Deployment

- **Git-based Version Control**: Managed via GitHub repository
- **Automated Setup**: Docker Compose for reliable deployment
- **Health Checks**: Built-in health monitoring for all services
- **Startup Scripts**: Automatic model loading and workflow import
- **Multi-profile Support**: GPU and CPU deployment options

## Key Components

### Docker Compose Setup
- Multi-profile configuration supporting GPU and CPU deployment
- Environment-based configuration using `.env`
- Automated service dependency management and health checks

### n8n Workflow Integration
- Pre-configured AI agent workflow
- Custom tools for Paperless API interaction
- Integrated Ollama model for intelligent processing
- API key authentication and endpoint management

### Environment Configuration
- Comprehensive variable setup in `.env`
- Service-specific versioning
- Security credentials and API keys
- GPU and AI model configuration

This architecture provides a complete document digitization pipeline with AI-powered search and management capabilities, suitable for personal or small business document workflows.
