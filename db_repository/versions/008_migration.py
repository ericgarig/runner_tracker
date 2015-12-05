from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
workout = Table('workout', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('athlete_id', Integer),
    Column('date', DateTime),
    Column('distance', Float),
    Column('speed', Float),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['workout'].columns['distance'].create()
    post_meta.tables['workout'].columns['speed'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['workout'].columns['distance'].drop()
    post_meta.tables['workout'].columns['speed'].drop()
