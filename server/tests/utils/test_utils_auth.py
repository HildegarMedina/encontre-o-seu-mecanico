from fastapi import HTTPException
from utils.auth import has_permissions
import pytest
import json

@pytest.mark.asyncio
async def test_has_permissions_failed():
    permissions = json.dumps({'MANAGE_USER': False})
    with pytest.raises(HTTPException) as exc_info:
        has_permissions(permissions, 'MANAGE_USER')
    assert exc_info.value.detail == 'You do not have permissions to manage user'