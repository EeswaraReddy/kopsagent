# Sample Confluence Page

## Overview
This is a sample Confluence page that demonstrates how to structure content for integration with the knowledgeops-agent project. It provides an example of how to document features, usage, and other relevant information.

## Features
- **Ingestion**: This project supports ingestion from various sources including Confluence, GitHub, and Slack.
- **Multi-Agent Orchestration**: The system is designed to handle multiple agents working together to process and retrieve information.
- **LLM Integration**: The project integrates with large language models for enhanced processing capabilities.

## Usage
To use the knowledgeops-agent, follow these steps:

1. **Setup**: Ensure you have the necessary dependencies installed as specified in `pyproject.toml`.
2. **Run the Application**: Use Docker to run the application locally with the provided `docker-compose.yml`.
3. **Access the API**: The FastAPI application exposes various endpoints for interaction. Refer to the API documentation for details.

## Example
Here is an example of how to use the ingestion endpoint:

```bash
curl -X POST http://localhost:8000/api/v1/ingest/confluence \
-H "Content-Type: application/json" \
-d '{"url": "https://your-confluence-page-url", "token": "your-api-token"}'
```

## Conclusion
This Confluence page serves as a template for documenting the knowledgeops-agent project. Modify the content as necessary to fit your specific use case and requirements.