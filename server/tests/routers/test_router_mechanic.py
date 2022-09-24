"""Router Client test file."""
import pytest
from mockups.mechanics import mechanics_mock

@pytest.mark.asyncio
async def test_register_new_mechanic(setup):
    """Test the /mechanic post route."""
    repo, client = setup
    
    response = await client.post("/mechanic", headers=None, json=mechanics_mock["john"])
    assert response.status_code == 201
