from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

FAKE_USERS_DB = {"admin": "admin123"}

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    if data.username not in FAKE_USERS_DB or FAKE_USERS_DB[data.username] != data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": data.username})
    return {"access_token": token}
