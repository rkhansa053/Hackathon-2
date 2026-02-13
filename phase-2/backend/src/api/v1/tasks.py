from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from uuid import UUID

from ...schemas.task import TaskCreate, TaskRead, TaskUpdate
from ...services.task_service import TaskService
from ...config.database import get_async_session
from .auth_deps import get_current_user
from ...models.user import User


router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def get_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get all tasks for a specific user."""
    # Verify that the requested user ID matches the current user ID
    try:
        requested_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    if current_user.id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    task_service = TaskService(session)
    tasks = await task_service.get_tasks_by_user(current_user.id)
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead)
async def create_task(
    user_id: str,
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new task for the user."""
    # Verify that the requested user ID matches the current user ID
    try:
        requested_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    if current_user.id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    task_service = TaskService(session)
    task = await task_service.create_task(current_user.id, task_create)
    return task


@router.get("/{user_id}/tasks/{id}", response_model=TaskRead)
async def get_task(
    user_id: str,
    id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get a specific task by ID."""
    # Verify that the requested user ID matches the current user ID
    try:
        requested_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    if current_user.id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    try:
        task_id = UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task_service = TaskService(session)
    task = await task_service.get_task_by_id_and_user(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{user_id}/tasks/{id}", response_model=TaskRead)
async def update_task(
    user_id: str,
    id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Update a specific task by ID."""
    # Verify that the requested user ID matches the current user ID
    try:
        requested_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    if current_user.id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    try:
        task_id = UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task_service = TaskService(session)
    task = await task_service.update_task(task_id, current_user.id, task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.delete("/{user_id}/tasks/{id}")
async def delete_task(
    user_id: str,
    id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Delete a specific task by ID."""
    # Verify that the requested user ID matches the current user ID
    try:
        requested_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    if current_user.id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    try:
        task_id = UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task_service = TaskService(session)
    success = await task_service.delete_task(task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskRead)
async def toggle_task_completion(
    user_id: str,
    id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Toggle the completion status of a task."""
    # Verify that the requested user ID matches the current user ID
    try:
        requested_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    if current_user.id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this task"
        )

    try:
        task_id = UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task_service = TaskService(session)
    task = await task_service.toggle_task_completion(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task