# import requests
import httpx
from os import environ
from fastapi import HTTPException

async def authenticate(token: str | None) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            headers = {"jwt-auth-token": token}
            print(token)
            response = await client.get("https://sac.prod.cluster.yanychoi.com/api/auth/user/authenticate", headers=headers)
            if response.status_code == 200:
                return True
        except:
            raise HTTPException(status_code=401, detail="Unauthorized")  
    # AUTH_URL = environ.get("AUTH_URL") or "https://sac.prod.cluster.yanychoi.com/api/auth"
    # if token is None:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    # auth_request = requests.get(f"{AUTH_URL}/user/authenticate", headers={"jwt-auth-token": token})
    # if auth_request.status_code == 200:
    #     return True
    # raise HTTPException(status_code=401, detail="Unauthorized")
    