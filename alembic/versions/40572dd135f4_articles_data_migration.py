"""articles_data_migration

Revision ID: 40572dd135f4
Revises: 0110f7d86a77
Create Date: 2023-07-10 11:14:05.666135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40572dd135f4'
down_revision = '0110f7d86a77'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            'article',
            sa.column('name', sa.VARCHAR(128)),
            sa.column('slug', sa.VARCHAR(64)),
            sa.column('description', sa.TEXT),
            sa.column('date_publish', sa.Date),
            sa.column('image', sa.VARCHAR(256)),
            sa.column('category_id', sa.INT)
        ),
        [
            {
                'name': 'Space',
                'slug': 'space',
                'description': 'Space description',
                'date_publish': 'Jan 2013, 13',
                'image': 'blog/space.jpg',
                'category_id': 1
            },
            {
                'name': 'Sport',
                'slug': 'sport',
                'description': 'Sport description',
                'date_publish': 'Jan 2015, 03',
                'image': 'blog/sport.jpg',
                'category_id': 2
            }
        ]
    )


def downgrade() -> None:
    pass
