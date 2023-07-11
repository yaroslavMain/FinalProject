"""caterory_data_migration

Revision ID: 0110f7d86a77
Revises: 97f9e4f24207
Create Date: 2023-07-10 11:13:19.117266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0110f7d86a77'
down_revision = '97f9e4f24207'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            'category',
            sa.column('name', sa.VARCHAR(64)),
            sa.column('slug', sa.VARCHAR(64)),
        ),
        [
            {'name': 'Space', 'slug': 'space'},
            {'name': 'Sport', 'slug': 'sport'},
        ]
    )


def downgrade() -> None:
    pass
