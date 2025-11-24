# Papercuts No More

[![Document Management](https://img.shields.io/badge/Document--Management-AI--Powered-blue)](https://github.com/aliuosio/papercuts-nomore)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

A comprehensive document digitization stack combining **Scanservjs** for scanning, **Paperless-ngx** for OCR processing, **n8n** for workflow automation, and **Ollama** for AI-powered analysis.
An n8n workflow with an ai agent to discuss with your documents is installed on first run of the setup.
works completely offline using ollama with Qwen3 as AI.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Optional: Scanner hardware, NVIDIA GPU

### Installation
```bash
git clone https://github.com/aliuosio/papercuts-no-more
cd papercuts-no-more
```

### Launch (GPU recommended)
```bash
docker compose --profile nvidia up -d
```

### Launch (CPU-only)
```bash
docker compose up -d
```

### Access Services

- **📄 Paperless-ngx**: http://localhost:8010 (admin/admin123)
- **⚙️ n8n Workflows**: http://localhost:5678
- **📷 Scanner**: http://localhost:8080
- **🤖 Ollama API**: http://localhost:11434

## 🏗️ Core Components

| Component | Function | Port | Technology |
|-----------|----------|------|------------|
| Paperless-ngx | Document management & OCR | 8010 | Django + PostgreSQL |
| n8n | Workflow automation & AI chat | 5678 | Node.js |
| Ollama | Local AI models | 11434 | Go + CUDA/CPU |
| Scanservjs | Document scanning | 8080 | Node.js |
| PostgreSQL | Data storage | 5432 | PostgreSQL |
| Redis | Caching & messaging | 6379 | Redis |

## 💡 Key Features

- **🔍 Intelligent Search**: Natural language queries via AI chat interface
- **⚡ GPU Acceleration**: Up to 500% faster AI processing
- **🔄 Automated Workflows**: n8n-powered document processing pipelines
- **📄 Multi-format Support**: PDF, images, office documents, scanned images
- **🏷️ Smart Categorization**: Automatic OCR and tagging
- **🔒 Secure Architecture**: Containerized services with authentication
- **🌐 German Language Support**: Optimized for German document processing

## 📖 Documentation

- **[Architecture Overview](.docs/architecture.md)** - System design and data flow
- **[Setup Guide](.docs/setup.md)** - Detailed installation and configuration
- **[API Documentation](.docs/api.md)** - REST API usage and authentication
- **[Deployment Guide](.docs/deployment.md)** - Production deployment and monitoring

## 🎯 Document Workflow

1. **Scan** → Use web scanner interface at port 8080
2. **Process** → Automatic OCR and metadata extraction
3. **Organize** → Tag, categorize, and search documents
4. **Automate** → Set up n8n workflows for processing
5. **Query** → Use AI chat for natural language search

## 🤖 AI Features

- **Local AI Processing**: Privacy-focused with Ollama
- **Natural Language Chat**: Ask questions like "Show me contracts from October"
- **Document Analysis**: AI-powered content understanding and summarization
- **Smart Classification**: Automated document tagging and routing

## 🔧 Configuration

Environment variables are managed via `.env` file. Key settings:

```bash
# AI Configuration
OLLAMA_MODEL=qwen3:8b
PAPERLESS_OCR_LANGUAGE=deu

# Authentication
PAPERLESS_ADMIN_USER=admin
PAPERLESS_ADMIN_PASSWORD=admin123
```

See [Setup Guide](.docs/setup.md) for complete configuration options.

## 🛠️ Development

```bash
# Development setup
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Run tests
docker compose exec webserver python manage.py test
```

See [Deployment Guide](.docs/deployment.md) for contribution guidelines and development workflow.

## 🏷️ Tags & Categories

- **Personal Use**: Document organization, receipt management, archiving
- **Business Use**: Invoice processing, contract management, compliance
- **Research**: Academic paper management, citation tracking
- **Legal**: Contract analysis, document versioning, audit trails

## 📊 Status & Health

Monitor system health:
```bash
docker compose ps                    # Service status
docker compose logs -f webserver    # Application logs
curl http://localhost:8010/api/health/  # Health check
```

## 📋 Version Information

- **Paperless-ngx**: v2.11.4
- **n8n**: v1.60.1
- **Ollama**: v0.3.12
- **AI Model**: qwen3:8b

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built on amazing open-source technologies:

- [Paperless-ngx](https://docs.paperless-ngx.com/) - Document management
- [n8n](https://n8n.io/) - Workflow automation
- [Ollama](https://ollama.ai/) - Local AI models
- [Scanservjs](https://github.com/sbs20/scanservjs) - Document scanning
