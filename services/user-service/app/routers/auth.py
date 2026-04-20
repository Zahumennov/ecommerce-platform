from fastapi import APIRouter, status

from app.dependencies import UserServiceDep
from app.schemas import LoginRequest, TokenResponse, UserRegister, UserResponse
from app.services.auth import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(data: UserRegister, service: UserServiceDep) -> UserResponse:
    user = await service.register(data)
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(data: LoginRequest, service: UserServiceDep) -> TokenResponse:
    user = await service.authenticate(data.email, data.password)
    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )