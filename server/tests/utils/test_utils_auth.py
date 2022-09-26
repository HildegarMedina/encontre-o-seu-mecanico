from fastapi import HTTPException
from utils.auth import verify_permissions
import pytest
import json

@pytest.mark.asyncio
async def test_verify_permissions_failed():
    permissions = json.dumps({'MANAGE_USER': False})
    with pytest.raises(HTTPException) as exc_info:
        verify_permissions(permissions, 'MANAGE_USER')
    assert exc_info.value.detail == 'You do not have permissions to manage user'