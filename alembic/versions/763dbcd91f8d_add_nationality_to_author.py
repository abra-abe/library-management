from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = '763dbcd91f8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add the 'nationality' column as nullable
    op.add_column('author', sa.Column('nationality', sa.String(), nullable=True))
    
    # Step 2: Provide a default value for existing rows
    op.execute("UPDATE author SET nationality = 'Unknown' WHERE nationality IS NULL")
    
    # Step 3: Alter the column to be NOT NULL
    op.alter_column('author', 'nationality', nullable=False)


def downgrade():
    # Reverse the changes made in the upgrade function
    op.drop_column('author', 'nationality')
