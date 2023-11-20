import httpx
from os import environ
from fastapi import HTTPException

async def authenticate(token: str | None) -> bool:
    async with httpx.AsyncClient() as client:
        AUTH_URL = environ.get("AUTH_URL") or "http://auth-service.auth-service.svc.cluster.local:8080/api/auth"
        try:
            headers = {"jwt-auth-token": token}
            print(token)
            response = await client.get(f"{AUTH_URL}/user/authenticate", headers=headers)
            if response.status_code == 200:
                return True
        except:
            raise HTTPException(status_code=401, detail="Unauthorized")
