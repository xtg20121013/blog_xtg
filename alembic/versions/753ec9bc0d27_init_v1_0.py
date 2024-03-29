# coding=utf-8
"""init_v1_0

Revision ID: 753ec9bc0d27
Revises: 
Create Date: 2017-03-12 20:17:20.958379

"""
from alembic import op
import sqlalchemy as sa
from model.constants import Constants

# revision identifiers, used by Alembic.
revision = '753ec9bc0d27'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    ats = op.create_table('articleTypeSettings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('protected', sa.Boolean(), nullable=True),
    sa.Column('hide', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    blog_info = op.create_table('blog_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('signature', sa.Text(), nullable=True),
    sa.Column('navbar', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blog_view',
    sa.Column('date', sa.DATE(), nullable=False),
    sa.Column('pv', sa.BigInteger(), nullable=True),
    sa.Column('uv', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('date')
    )
    op.create_table('menus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    plugins = op.create_table('plugins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_plugins_order'), 'plugins', ['order'], unique=False)
    sources = op.create_table('sources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    articleTypes = op.create_table('articleTypes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('introduction', sa.Text(), nullable=True),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('setting_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
    sa.ForeignKeyConstraint(['setting_id'], ['articleTypeSettings.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('num_of_view', sa.Integer(), nullable=True),
    sa.Column('articleType_id', sa.Integer(), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['articleType_id'], ['articleTypes.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_articles_create_time'), 'articles', ['create_time'], unique=False)
    op.create_index(op.f('ix_articles_update_time'), 'articles', ['update_time'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('author_name', sa.String(length=64), nullable=True),
    sa.Column('author_email', sa.String(length=64), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('comment_type', sa.String(length=64), nullable=True),
    sa.Column('rk', sa.String(length=64), nullable=True),
    sa.Column('floor', sa.Integer(), nullable=False),
    sa.Column('reply_to_id', sa.Integer(), nullable=True),
    sa.Column('reply_to_floor', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
    # insert default data
    op.bulk_insert(ats, [
        dict(id=1, name='system', protected=True, hide=True)
    ])
    op.bulk_insert(blog_info,[
        dict(id=1,
             title=u'开源分布式博客系统blog_xtg',
             signature=u'基于tornado的分布式博客！— by xtg',
             navbar='inverse')
    ])
    op.bulk_insert(plugins, [
        dict(id=1,
             title=u'博客统计',
             note=u'系统插件',
             content='system_plugin',
             order=1,
             disabled=False)
    ])
    op.bulk_insert(sources, [
        dict(id=1, name=u'原创', ),
        dict(id=2, name=u'转载', ),
        dict(id=3, name=u'翻译', ),
    ])
    op.bulk_insert(articleTypes, [
        dict(id=Constants.ARTICLE_TYPE_DEFAULT_ID,
             name=u'未分类',
             introduction=u'系统默认分类，不可删除。',
             setting_id=1,
        ),
    ])


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_index(op.f('ix_articles_update_time'), table_name='articles')
    op.drop_index(op.f('ix_articles_create_time'), table_name='articles')
    op.drop_table('articles')
    op.drop_table('articleTypes')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('sources')
    op.drop_index(op.f('ix_plugins_order'), table_name='plugins')
    op.drop_table('plugins')
    op.drop_table('menus')
    op.drop_table('blog_view')
    op.drop_table('blog_info')
    op.drop_table('articleTypeSettings')
    # ### end Alembic commands ###
