FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --no-dev

# Copy the source code
COPY src/knowledgeops /app/src/knowledgeops

# Expose the FastAPI port
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "uvicorn", "src.knowledgeops.main:app", "--host", "0.0.0.0", "--port", "8000"]