import uuid

from fastapi import APIRouter, status

from app.dependencies import CurrentUser, UserServiceDep
from app.schemas import MessageResponse, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(current_user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.patch(
    "/me",
    response_model=UserResponse,
)
async def update_me(
    data: UserUpdate,
    current_user: CurrentUser,
    service: UserServiceDep,
) -> UserResponse:
    user = await service.update(current_user, data)
    return UserResponse.model_validate(user)


@router.delete(
    "/me",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_me(
    current_user: CurrentUser,
    service: UserServiceDep,
) -> MessageResponse:
    await service.delete(current_user)
    return MessageResponse(message="Account deleted successfully")


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(user_id: uuid.UUID, service: UserServiceDep) -> UserResponse:
    user = await service.get_by_id(user_id)
    return UserResponse.model_validate(user)