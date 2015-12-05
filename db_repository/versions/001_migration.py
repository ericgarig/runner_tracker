from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
athlete = Table('athlete', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name_first', VARCHAR(length=64)),
    Column('name_last', VARCHAR(length=64)),
    Column('nickname', VARCHAR(length=64)),
    Column('phone_number', VARCHAR(length=10)),
    Column('ice_name', VARCHAR(length=64)),
    Column('ice_phone', VARCHAR(length=10)),
)

workout = Table('workout', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('athlete_id', INTEGER),
    Column('date', DATETIME),
    Column('distance', INTEGER),
    Column('speed', DATETIME),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['athlete'].drop()
    pre_meta.tables['workout'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['athlete'].create()
    pre_meta.tables['workout'].create()
