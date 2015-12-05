from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
athlete = Table('athlete', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name_first', String(length=64)),
    Column('name_last', String(length=64)),
    Column('nickname', String(length=64)),
    Column('phone_number', String(length=10)),
    Column('ice_name', String(length=64)),
    Column('ice_phone', String(length=10)),
)

workout = Table('workout', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('athlete_id', Integer),
    Column('date', DateTime),
    Column('distance', Integer),
    Column('speed', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['athlete'].create()
    post_meta.tables['workout'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['athlete'].drop()
    post_meta.tables['workout'].drop()
