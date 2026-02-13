from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from uuid import UUID

from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User
from fastapi import HTTPException, status


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, user_id: UUID, task_create: TaskCreate) -> Task:
        """Create a new task for a user."""
        # Verify user exists
        user = await self._get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Create the task
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=user_id
        )

        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)

        return db_task

    async def get_tasks_by_user(self, user_id: UUID) -> List[Task]:
        """Get all tasks for a specific user."""
        statement = select(Task).where(Task.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_task_by_id_and_user(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Get a specific task by ID and user ID."""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def update_task(self, task_id: UUID, user_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
        """Update a specific task by ID and user ID."""
        db_task = await self.get_task_by_id_and_user(task_id, user_id)
        if not db_task:
            return None

        # Update the task with non-None values
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)

        return db_task

    async def delete_task(self, task_id: UUID, user_id: UUID) -> bool:
        """Delete a specific task by ID and user ID."""
        db_task = await self.get_task_by_id_and_user(task_id, user_id)
        if not db_task:
            return False

        await self.session.delete(db_task)
        await self.session.commit()

        return True

    async def toggle_task_completion(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Toggle the completion status of a task."""
        db_task = await self.get_task_by_id_and_user(task_id, user_id)
        if not db_task:
            return None

        db_task.completed = not db_task.completed
        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)

        return db_task

    async def _get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()