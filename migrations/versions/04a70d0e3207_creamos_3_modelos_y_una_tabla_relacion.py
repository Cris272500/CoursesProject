"""creamos 3 modelos y una tabla relacion

Revision ID: 04a70d0e3207
Revises: 
Create Date: 2024-06-22 09:53:57.248036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04a70d0e3207'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categoria',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('curso',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=100), nullable=False),
    sa.Column('email_user', sa.String(length=60), nullable=False),
    sa.Column('rol', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email_user'),
    sa.UniqueConstraint('username')
    )
    op.create_table('categorias_curso',
    sa.Column('curso_id', sa.Integer(), nullable=False),
    sa.Column('categoria_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['categoria_id'], ['categoria.id'], ),
    sa.ForeignKeyConstraint(['curso_id'], ['curso.id'], ),
    sa.PrimaryKeyConstraint('curso_id', 'categoria_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('categorias_curso')
    op.drop_table('usuario')
    op.drop_table('curso')
    op.drop_table('categoria')
    # ### end Alembic commands ###
