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
    Column('address_city', VARCHAR(length=64)),
    Column('address_state', VARCHAR(length=2)),
    Column('address_street', VARCHAR(length=64)),
    Column('address_zip', VARCHAR(length=5)),
    Column('date_birth', DATE),
    Column('disability', VARCHAR(length=64)),
    Column('email', VARCHAR(length=64)),
    Column('notes', TEXT),
    Column('pace', FLOAT),
)

athlete = Table('athlete', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name_first', String(length=64)),
    Column('name_last', String(length=64)),
    Column('nickname', String(length=64)),
    Column('phone_number', String(length=10)),
    Column('ice_name', String(length=64)),
    Column('ice_phone', String(length=10)),
    Column('note', Text),
    Column('date_birth', Date),
    Column('email', String(length=64)),
    Column('disability', String(length=64)),
    Column('pace', Float),
    Column('address_street', String(length=64)),
    Column('address_city', String(length=64)),
    Column('address_state', String(length=2)),
    Column('address_zip', String(length=5)),
)

workout = Table('workout', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('athlete_id', INTEGER),
    Column('distance', FLOAT),
    Column('speed', FLOAT),
    Column('date', DATE),
    Column('notes', TEXT),
)

workout = Table('workout', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('athlete_id', Integer),
    Column('date', Date),
    Column('distance', Float),
    Column('speed', Float),
    Column('note', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['athlete'].columns['notes'].drop()
    post_meta.tables['athlete'].columns['note'].create()
    pre_meta.tables['workout'].columns['notes'].drop()
    post_meta.tables['workout'].columns['note'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['athlete'].columns['notes'].create()
    post_meta.tables['athlete'].columns['note'].drop()
    pre_meta.tables['workout'].columns['notes'].create()
    post_meta.tables['workout'].columns['note'].drop()
