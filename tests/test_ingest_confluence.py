import pytest
from src.knowledgeops.connectors.confluence import ConfluenceConnector

@pytest.fixture
def confluence_connector():
    return ConfluenceConnector(api_token="test_token", base_url="https://test.confluence.com")

def test_ingest_confluence(confluence_connector):
    # Assuming the connector has a method called `ingest` that returns a success message
    response = confluence_connector.ingest(page_id="12345")
    assert response == "Ingestion successful for page ID: 12345"

def test_ingest_confluence_invalid_page(confluence_connector):
    # Test for invalid page ID
    response = confluence_connector.ingest(page_id="invalid_id")
    assert response == "Error: Page not found"