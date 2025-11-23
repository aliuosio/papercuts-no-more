# Codebase Overview: Papercuts No More

## Project Summary

Papercuts No More is a comprehensive document digitization stack built with Docker Compose. It integrates multiple services for end-to-end document processing: scanning (Scanservjs), management and OCR (Paperless-ngx), workflow automation (n8n), and AI-powered analysis (Ollama).

## Architecture Overview

- **Docker-based deployment**: Multi-service architecture using Docker Compose
- **Document flow**: Scan → Consume → Process/OCR → Organize → Automate → AI Analyze
- **Services**:
  - Scanservjs: Document scanning interface
  - Paperless-ngx: Document management with OCR and database storage
  - n8n: Workflow automation platform
  - Ollama: Local AI model server for document analysis
  - PostgreSQL: Data storage
  - Redis: Caching and message queuing

## Key Features

- Automated document ingestion from scanner
- OCR processing and searchable text extraction
- Document organization with tagging and metadata
- REST API for programmatic access
- AI-powered chat interface for natural language queries
- Configurable GPU support (Nvidia/CPU modes)

## Directory Structure

- `mcp-servers/`: Collection of MCP (Model Context Protocol) server implementations
  - everything: Comprehensive MCP server
  - fetch: HTTP request capabilities
  - filesystem: File system operations
  - git: Git operations
  - memory: Knowledge/memory management
  - sequentialthinking: Step-by-step reasoning
  - time: Time/date utilities
- `n8n_shared/`: Pre-configured n8n workflow definitions
- `.docker/`: Docker volume mappings and configurations
- `.docs/`: Project documentation

## Technology Stack

- Containers: Docker Compose
- Document Processing: Paperless-ngx, OCR
- Automation: n8n workflows
- AI: Ollama with configurable models
- APIs: REST-based with API key authentication

## Last Analyzed

2025-11-23

## Notable Patterns

- Modular service architecture
- MCP server integration for extensible automation
- Environment-based configuration (.env)
- Automated workflow imports
