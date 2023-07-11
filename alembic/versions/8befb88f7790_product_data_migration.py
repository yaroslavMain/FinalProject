"""product_data_migration

Revision ID: 8befb88f7790
Revises: 40572dd135f4
Create Date: 2023-07-10 11:14:40.506597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8befb88f7790'
down_revision = '40572dd135f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table(
            'product',
            sa.column('name', sa.VARCHAR(128)),
            sa.column('price', sa.DECIMAL(8, 2)),
            sa.column('image', sa.VARCHAR(256))
        ),
        [
            {
                'name': 'Egronomic Chair',
                'price': 50,
                'image': 'shop/product-3.png'
            },
            {
                'name': 'Nordic Chair',
                'price': 49,
                'image': 'shop/product-1.png'
            },
            {
                'name': 'Kruzo Aero Chair',
                'price': 75,
                'image': 'shop/product-2.png'
            }
        ]
    )


def downgrade() -> None:
    pass
