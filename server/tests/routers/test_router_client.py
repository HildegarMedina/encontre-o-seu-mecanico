"""Router Client test file."""
import pytest
from mockups.clients import clients_mock

@pytest.mark.asyncio
async def test_register_new_client(setup):
    """Test the /client post route."""
    repo, client = setup
    
    response = await client.post("/client", headers=None, json=clients_mock["john"])
    assert response.status_code == 201
