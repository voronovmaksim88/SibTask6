import secrets
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo-auth", tags=["demo-auth"])

security = HTTPBasic()


@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message": "Hi,",
        "username": credentials.username,
        "password": credentials.password,
    }


usernames_to_passwords = {"admin": "admin", "max": "qwerty"}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauthed_exec = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid user name or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exec

    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exec

    return credentials.username


@router.get("/basic-auth-username/")
def demo_basic_auth_user(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hi,{auth_username}",
        "username": auth_username,
    }
