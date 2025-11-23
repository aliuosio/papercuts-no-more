# API Documentation

This document provides comprehensive information about the Paperless-ngx REST API and authentication methods used in Papercuts No More.

## API Overview

Paperless-ngx provides a RESTful API for document management operations. The API is accessible both externally and internally within the Docker network.

### Base URLs

- **External Access**: `http://localhost:8010/api/`
- **Internal Access** (from n8n): `http://webserver:8000/api/`

### API Version

The API follows REST principles and returns JSON responses. All endpoints require authentication.

## Authentication Methods

### 1. Basic Authentication (Recommended)

**Status**: ✅ **Currently Working**

This method uses HTTP Basic Authentication as implemented in Paperless-ngx.

#### Configuration
```http
Authorization: Basic <base64-encoded-credentials>
```

Example in curl:
```bash
curl -u admin:admin123 http://localhost:8010/api/documents/
```

#### n8n Configuration
When configuring HTTP Request nodes in n8n, use:
- **Authentication**: Basic Auth
- **Username**: `admin`
- **Password**: `admin123`

### 2. Token Authentication

**Status**: ✅ **Working**

Obtain a token first, then use it for subsequent requests.

#### Token Acquisition
```http
POST /api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response**:
```json
{
  "token": "your_token_here"
}
```

#### Using the Token
```http
GET /api/documents/
Authorization: Token your_token_here
```

### 3. Custom X-API-Key Authentication

**Status**: ❌ **Planned - Not Currently Active**

Custom authentication requires additional setup scripts to enable.

#### Intended Usage
```http
GET /api/documents/
X-API-Key: your_api_key_here
```

#### Implementation Status
- Custom authentication scripts not currently in project
- Requires creation of `/.docker/custom-auth/` directory with authentication logic
- Falls back to standard token authentication when not configured

## Core API Endpoints

### Documents

#### List Documents
```http
GET /api/documents/
```

**Parameters**:
- `page` - Page number (pagination)
- `page_size` - Results per page (default: 25, max: 100)
- `query` - Full-text search query
- `ordering` - Sort field (e.g., `created`, `title`, `-modified`)
- `tags__id` - Filter by tag ID
- `document_type__id` - Filter by document type
- `correspondent__id` - Filter by correspondent
- `created_date__date__gte` - Created after date (YYYY-MM-DD)
- `created_date__date__lte` - Created before date (YYYY-MM-DD)

**Example Request**:
```bash
curl -u admin:admin123 "http://localhost:8010/api/documents/?query=insurance&page=1"
```

#### Get Single Document
```http
GET /api/documents/{id}/
```

Returns detailed document information including:
- Metadata (title, created date, etc.)
- Content (OCR text)
- Tags, correspondent, document type

#### Upload Document
```http
POST /api/documents/post_document/
Content-Type: multipart/form-data

Form Data:
- document: (file)
- title: (optional)
- tags: (optional, JSON array)
```

#### Download Document
```http
GET /api/documents/{id}/download/
```

Returns the original document file.

### Tags

#### List Tags
```http
GET /api/tags/
```

#### Create Tag
```http
POST /api/tags/
Content-Type: application/json

{
  "name": "Important",
  "color": "#FF0000",
  "matching_algorithm": "auto"
}
```

#### Update Tag
```http
PUT /api/tags/{id}/
```

#### Delete Tag
```http
DELETE /api/tags/{id}/
```

### Document Types

#### List Document Types
```http
GET /api/document_types/
```

#### Create Document Type
```http
POST /api/document_types/
Content-Type: application/json

{
  "name": "Contract"
}
```

### Correspondents

#### List Correspondents
```http
GET /api/correspondents/
```

#### Create Correspondent
```http
POST /api/correspondents/
Content-Type: application/json

{
  "name": "ABC Insurance"
}
```

## Advanced API Usage

### Full-Text Search

Paperless-ngx includes powerful full-text search capabilities:

```bash
# Search for documents containing "policy"
curl -u admin:admin123 "http://localhost:8010/api/documents/?query=policy"

# Search in specific date range
curl -u admin:admin123 "http://localhost:8010/api/documents/?query=tax&created_date__date__gte=2023-01-01&created_date__date__lte=2023-12-31"
```

### Bulk Operations

#### Bulk Tag Assignment
```http
PUT /api/documents/{id}/
Content-Type: application/json

{
  "tags": [1, 2, 3]
}
```

### Filtering and Sorting

Advanced filtering options:

```bash
# Filter by multiple criteria
curl -u admin:admin123 "http://localhost:8010/api/documents/?tags__id=5&document_type__id=2&correspondent__id=3"

# Sort by creation date (descending)
curl -u admin:admin123 "http://localhost:8010/api/documents/?ordering=-created"

# Combine search with filters
curl -u admin:admin123 "http://localhost:8010/api/documents/?query=invoice&created_date__date__gte=2024-01-01&ordering=created"
```

## n8n Integration Examples

### Basic Document Query Workflow

1. **HTTP Request Node**:
   ```
   Method: GET
   URL: http://webserver:8000/api/documents/
   Authentication: Basic Auth
   Username: admin
   Password: admin123
   Query Parameters:
   - Key: query, Value: {{ $json.query }}
   - Key: page_size, Value: 10
   ```

2. **Ollama Chat Model Node**:
   ```
   Base URL: http://ollama-nvidia:11434 (or http://ollama:11434)
   Model: qwen3:8b
   Messages: "Analyze these documents and provide a summary..."
   ```

### Document Upload Workflow

1. **HTTP Request Node** (POST):
   ```
   Method: POST
   URL: http://webserver:8000/api/documents/post_document/
   Authentication: Basic Auth
   Body Content Type: Multipart-Form-Data
   Parameters:
   - Name: document, Value: {{ $binary.data }}
   - Name: title, Value: {{ $json.title }}
   ```

### AI-Powered Document Analysis

1. **HTTP Request Node** (fetch documents)
2. **Function Node** (extract text content)
3. **Ollama Chat Model Node** (analyze content)
4. **HTTP Request Node** (update document metadata/tags)

## Error Handling

### Common HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (invalid credentials)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

### Authentication Errors

**401 Unauthorized** responses typically indicate:
- Incorrect username/password for Basic Auth
- Invalid or expired token
- Missing authentication headers

### Rate Limiting

Paperless-ngx doesn't implement explicit rate limiting, but consider:
- Reasonable delays between requests in automation workflows
- Batch operations for bulk processing
- Error handling and retry logic in n8n workflows

## Best Practices

### Authentication
1. Use Basic Auth in n8n for simplicity and reliability
2. Store credentials securely (avoid hardcoding in workflows)
3. Implement proper error handling for authentication failures

### API Usage
1. Use pagination for large result sets (`page_size` parameter)
2. Implement caching to reduce API load
3. Batch operations when possible
4. Handle rate limits and temporary failures gracefully

### Performance Optimization
1. Use specific filters to reduce result sets
2. Cache frequently accessed data
3. Implement retry logic for transient failures
4. Monitor API response times and adjust workflow complexity

### Security
1. Never expose API credentials in logs or error messages
2. Use HTTPS when accessing APIs over external networks
3. Regularly rotate API keys and passwords
4. Implement proper access controls at the application level

## Troubleshooting

### Authentication Issues

**Problem**: 401 Unauthorized error
**Solutions**:
- Verify username/password are correct
- Check if using Basic Auth vs Token Auth correctly
- Ensure proper headers are set

**Problem**: API key authentication not working
**Cause**: Custom authentication not configured
**Solution**: Implement custom authentication scripts (future feature)

### Connection Issues

**Problem**: Connection refused
**Solutions**:
- Verify service URLs (internal vs external)
- Check if services are running (`docker compose ps`)
- Confirm port accessibility

**Problem**: Timeout errors
**Causes**: Large result sets, slow queries
**Solutions**:
- Increase timeout in HTTP request nodes
- Use pagination to reduce response size
- Optimize query filters

### Data Issues

**Problem**: Documents not appearing in search
**Solutions**:
- Wait for OCR processing to complete
- Check document upload status
- Verify OCR language settings

**Problem**: Bulk operations failing
**Solutions**:
- Reduce batch sizes
- Implement proper error handling
- Check API rate limits

## API Reference

For complete API documentation, refer to:
- Official Paperless-ngx API docs: Consult the built-in API documentation
- Interactive API browser: Available at `/api/docs/` when authenticated
- OpenAPI specification: Available at `/api/schema/` (JSON format)

## Examples Repository

See the `n8n_shared/` directory for complete workflow examples demonstrating:
- Document querying and analysis
- Automated tagging workflows
- AI-powered document classification
- Bulk document processing operations
