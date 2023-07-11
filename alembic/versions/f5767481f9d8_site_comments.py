"""site comments

Revision ID: f5767481f9d8
Revises: 8befb88f7790
Create Date: 2023-07-10 12:14:21.483001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5767481f9d8'
down_revision = '8befb88f7790'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            'testimonial',
            sa.column('body', sa.VARCHAR(256)),
            sa.column('name', sa.VARCHAR(64)),
        ),
        [
            {
                'body': "It's a good store!",
                'name': 'Vasya',
            },
            {
                'body': 'Good quality goods!',
                'name': 'Andrey',
            }
        ]
    )


def downgrade() -> None:
    pass
