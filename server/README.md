# ConfReady Server

This directory contains the backend server for ConfReady, an AI-powered solution for filling out conference checklists.

## Features

- Processes LaTeX documents (.tex, .zip, .tar.gz)
- Supports multiple conference checklists:
  - ACL Responsible NLP Research Checklist
  - NeurIPS Paper Checklist
  - NeurIPS Datasets & Benchmarks Checklist
- Uses advanced retrieval and reranking for accurate responses

## Development Mode

For faster testing and development, you can enable DEV_MODE to process only the first 3 questions:

### Setting DEV_MODE

```bash
# Enable DEV_MODE
export DEV_MODE=true

# Disable DEV_MODE (default)
export DEV_MODE=false
```

### What DEV_MODE Does

When DEV_MODE is enabled, the system will only process the first 3 questions for each checklist type:

- **ACL**: A1, A2, A3
- **NeurIPS**: 1, 2, 3
- **NeurIPS D&B**: 1a, 1b, 1c

This significantly reduces processing time and API costs during development.

### Usage Example

```bash
# Start the server with DEV_MODE enabled
DEV_MODE=true python app.py

# Or set it in your environment
export DEV_MODE=true
python app.py
```

## Environment Variables

Required environment variables:
- `TOGETHERAI_API_KEY`: Your Together AI API key
- `OPENAI_API_KEY`: Your OpenAI API key (optional, for some features)

Optional environment variables:
- `DEV_MODE`: Set to 'true' to enable development mode (default: 'false')

## Running the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

The server will run on `http://localhost:8080`

## API Endpoints

- `POST /api/upload`: Upload and process LaTeX documents
- `GET /api/upload/status`: Get processing status updates
- `POST /api/upload/status/update`: Update processing status
- `GET /api/helloworld`: Health check endpoint 