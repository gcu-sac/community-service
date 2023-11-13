import requests
from fastapi import HTTPException

def authenticate(token: str | None) -> bool:
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    auth_request = requests.get(f"/user/authenticate", cookies={"jwtAuthToken": token})
    if auth_request.status_code == 200:
        return True
    raise HTTPException(status_code=401, detail="Unauthorized")
    