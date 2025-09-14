# Architecture Overview

## Introduction
The KnowledgeOps Agent is designed to facilitate the ingestion, processing, and retrieval of knowledge from various sources, leveraging modern technologies such as FastAPI, PostgreSQL, and Chroma. This document outlines the architecture of the system, including its components, interactions, and deployment strategies.

## System Components

### 1. FastAPI Application
The core of the KnowledgeOps Agent is a FastAPI application that serves as the main entry point for handling API requests. It is responsible for routing requests to the appropriate endpoints and managing the application lifecycle.

### 2. API Endpoints
The application exposes a set of REST API endpoints organized under versioned paths. The primary endpoints include:
- **Chat Endpoint**: Facilitates user queries and interactions.
- **Ingestion Endpoints**: Handles data ingestion from various sources such as Confluence and GitHub.

### 3. Connectors
Connectors are specialized modules responsible for interfacing with external systems. The current implementation includes:
- **Confluence Connector**: Ingests data from Confluence using an API token.
- **GitHub Connector**: Manages data ingestion from GitHub, including webhook support.

### 4. Ingestion Logic
The ingestion module contains the logic for parsing and processing the ingested data. It includes:
- **Generic Parser**: A chunker and embedding mechanism for processing text.
- **Terraform Parser**: Parses Terraform configurations and extracts metadata.
- **Helm Parser**: Handles Helm chart values and configurations.

### 5. Storage
The storage module is responsible for persisting the ingested data. It includes:
- **Vector Store**: A wrapper around Chroma/PGVector for storing vector representations of data.
- **Metadata Store**: Implements ORM models for managing metadata in PostgreSQL.

### 6. Agents
The multi-agent orchestration system coordinates various tasks within the application. It includes:
- **Orchestrator**: Manages the workflow from planning to execution.
- **Retriever**: Implements logic for retrieving relevant information based on user queries.

### 7. LLM Integration
The system integrates with large language models (LLMs) to enhance its capabilities. The current implementation includes a wrapper for the Groq LLM API.

### 8. User Interface
A demo user interface is built using Streamlit, providing a simple way for users to interact with the KnowledgeOps Agent.

## Deployment
The application is designed for local development using Docker Compose, which orchestrates the necessary services, including PostgreSQL and Chroma. For production deployments, a Helm chart is provided for Kubernetes, allowing for scalable and manageable deployments.

## Infrastructure
The infrastructure can be bootstrapped using Terraform, providing an optional setup for provisioning cloud resources.

## Conclusion
The KnowledgeOps Agent is a modular and extensible system designed to facilitate knowledge ingestion and retrieval. Its architecture supports easy integration with various data sources and provides a robust framework for future enhancements.