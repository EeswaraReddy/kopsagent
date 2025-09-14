import pytest
from src.knowledgeops.connectors.github import GitHubConnector

@pytest.fixture
def github_connector():
    return GitHubConnector(api_token="test_token")

def test_github_ingestion(github_connector):
    # Assuming the GitHubConnector has a method called `ingest`
    result = github_connector.ingest("test_repo")
    assert result is not None
    assert isinstance(result, dict)  # Assuming the result is a dictionary

def test_github_webhook(github_connector):
    # Assuming the GitHubConnector has a method called `handle_webhook`
    webhook_data = {"action": "created", "repository": {"name": "test_repo"}}
    response = github_connector.handle_webhook(webhook_data)
    assert response == "Webhook processed successfully"  # Adjust based on actual response

def test_invalid_token():
    with pytest.raises(ValueError):
        GitHubConnector(api_token="invalid_token")  # Assuming it raises ValueError for invalid token