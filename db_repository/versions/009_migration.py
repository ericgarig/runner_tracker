from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
workout = Table('workout', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('athlete_id', INTEGER),
    Column('date', DATETIME),
    Column('distance', FLOAT),
    Column('speed', FLOAT),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['workout'].columns['date'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['workout'].columns['date'].create()
