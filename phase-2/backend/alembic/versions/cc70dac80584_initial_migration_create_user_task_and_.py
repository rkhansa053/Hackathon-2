"""Initial migration: create user, task, and refresh_token tables

Revision ID: cc70dac80584
Revises: 
Create Date: 2026-02-07 23:43:38.592881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc70dac80584'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: create user, task, and refresh_token tables."""
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    # Create index on email for faster lookups
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)

    # Create task table
    op.create_table(
        'task',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    # Create index on user_id for efficient user task queries
    op.create_index(op.f('ix_task_user_id'), 'task', ['user_id'], unique=False)

    # Create refresh_token table
    op.create_table(
        'refreshtoken',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('token_hash', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    # Create index on user_id for efficient token lookups
    op.create_index(op.f('ix_refreshtoken_user_id'), 'refreshtoken', ['user_id'], unique=False)
    # Create index on token_hash for efficient token validation
    op.create_index(op.f('ix_refreshtoken_token_hash'), 'refreshtoken', ['token_hash'], unique=False)


def downgrade() -> None:
    """Downgrade schema: drop all tables."""
    # Drop tables in reverse order
    op.drop_index(op.f('ix_refreshtoken_token_hash'), table_name='refreshtoken')
    op.drop_index(op.f('ix_refreshtoken_user_id'), table_name='refreshtoken')
    op.drop_table('refreshtoken')

    op.drop_index(op.f('ix_task_user_id'), table_name='task')
    op.drop_table('task')

    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
