import requests
from os import environ
from fastapi import HTTPException

def authenticate(token: str | None) -> bool:
    AUTH_URL = environ.get("AUTH_URL") or "https://sac.prod.cluster.yanychoi.com/api/auth"
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    auth_request = requests.get(f"{AUTH_URL}/user/authenticate", headers={"jwt-auth-token": token})
    if auth_request.status_code == 200:
        return True
    raise HTTPException(status_code=401, detail="Unauthorized")
    