from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.auth import decode_access_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = decode_access_token(token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user
from fastapi import HTTPException


def require_role(required_role: str):

    def role_checker(current_user = Depends(get_current_user)):

        if current_user.role != required_role:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return current_user

    return role_checker