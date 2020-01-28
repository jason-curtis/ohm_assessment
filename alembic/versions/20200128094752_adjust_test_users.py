"""adjust test users

Revision ID: 477d0d895c4f
Revises: 00000000
Create Date: 2020-01-28 09:47:52.185366

Increase the point_balance for user 1 to 5000
Add a location for user 2, assuming they live in the USA
Change the tier for user 3 to Silver
"""

# revision identifiers, used by Alembic.
revision = '477d0d895c4f'
down_revision = '00000000'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('''UPDATE user
        SET point_balance = 5000
        WHERE user_id = 1
    ''')
    op.execute('''UPDATE user
        SET tier = 'Silver'
        WHERE user_id = 3
    ''')

    op.execute('''ALTER TABLE user
        ADD country varchar(255)
    ''')
    op.execute('''UPDATE user
        SET country = 'USA'
        WHERE user_id = 2
    ''')


def downgrade():
    op.execute('''ALTER TABLE user
        DROP COLUMN country
    ''')
