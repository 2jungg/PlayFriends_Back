from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

from app.schemas.group import GroupCreate, GroupUpdate, GroupResponse, GroupList, Message
from app.models.user import UserModel
from app.services.group_service import GroupService
from app.schemas.category import CategoryListResponse
from app.schemas.schedule import ScheduleResponse
from app.db.session import get_db
from app.core.security import get_current_user

router = APIRouter()

def get_group_service(db: AsyncIOMotorClient = Depends(get_db)) -> GroupService:
    return GroupService(db)

@router.post("/groups/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    group_data: GroupCreate,
    service: GroupService = Depends(get_group_service),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Create a new group.
    """
    new_group = await service.create_group(group_data, current_user.id)
    return new_group

@router.get("/groups/", response_model=GroupList)
async def get_all_groups(
    service: GroupService = Depends(get_group_service)
):
    """
    Get all groups.
    """
    groups = await service.get_all_groups()
    return {"groups": groups}

@router.get("/groups/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: str,
    service: GroupService = Depends(get_group_service)
):
    """
    Get a single group by ID.
    """
    group = await service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return group

@router.put("/groups/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: str,
    group_data: GroupUpdate,
    service: GroupService = Depends(get_group_service),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Update a group. Only the owner can update the group.
    """
    group = await service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if group.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this group")
    
    updated_group = await service.update_group(group_id, group_data)
    return updated_group

@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: str,
    service: GroupService = Depends(get_group_service),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Delete a group. Only the owner can delete the group.
    """
    group = await service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if group.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this group")

    success = await service.delete_group(group_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete group")
    return


@router.post("/groups/{group_id}/join", response_model=Message, status_code=status.HTTP_200_OK)
async def join_group(
    group_id: str,
    service: GroupService = Depends(get_group_service),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Join a group.
    """
    group = await service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    success = await service.add_member(group_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to join group. You might already be in the group or user not found.")
    return {"message": "Successfully joined the group"}


@router.delete("/groups/{group_id}/leave", response_model=Message, status_code=status.HTTP_200_OK)
async def leave_group(
    group_id: str,
    service: GroupService = Depends(get_group_service),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Leave a group.
    """
    group = await service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    if group.owner_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner cannot leave the group. You must delete the group instead.")

    success = await service.remove_member(group_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to leave group. You might not be in the group.")
    return {"message": "Successfully left the group"}

@router.post("/groups/{group_id}/recommend-categories", response_model=CategoryListResponse)
async def recommend_categories(
    group_id: str,
    service: GroupService = Depends(get_group_service),
    # current_user: UserModel = Depends(get_current_user)
):
    """
    Recommend play categories for a group based on member preferences.
    Only the group owner can request recommendations.
    """
    group = await service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    # if group.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the group owner can get recommendations")

    categories = await service.recommend_categories(group_id)
    return {"categories": categories}

@router.post("/groups/{group_id}/schedules", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    group_id: str,
    category_ids: List[str] = Body(..., embed=True),
    service: GroupService = Depends(get_group_service),
    # current_user: UserModel = Depends(get_current_user)
):
    """
    Create a schedule for a group based on selected categories.
    Any member of the group can create a schedule.
    """
    group = await service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    # if current_user.id not in group.member_ids:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only group members can create a schedule")
    schedule = await service.create_schedule_from_categories(group_id, category_ids)
    if not schedule:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create schedule. Check group times or selected categories.")
    return schedule
