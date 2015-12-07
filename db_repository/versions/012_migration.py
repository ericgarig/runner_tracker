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
    Column('notes', Text),
    Column('date_birth', Date),
    Column('email', String(length=64)),
    Column('disability', String(length=64)),
    Column('pace', Float),
    Column('address_street', String(length=64)),
    Column('address_city', String(length=64)),
    Column('address_state', String(length=2)),
    Column('address_zip', String(length=5)),
)

workout = Table('workout', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('athlete_id', Integer),
    Column('date', Date),
    Column('distance', Float),
    Column('speed', Float),
    Column('notes', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['athlete'].columns['address_city'].create()
    post_meta.tables['athlete'].columns['address_state'].create()
    post_meta.tables['athlete'].columns['address_street'].create()
    post_meta.tables['athlete'].columns['address_zip'].create()
    post_meta.tables['athlete'].columns['date_birth'].create()
    post_meta.tables['athlete'].columns['disability'].create()
    post_meta.tables['athlete'].columns['email'].create()
    post_meta.tables['athlete'].columns['notes'].create()
    post_meta.tables['athlete'].columns['pace'].create()
    post_meta.tables['workout'].columns['notes'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['athlete'].columns['address_city'].drop()
    post_meta.tables['athlete'].columns['address_state'].drop()
    post_meta.tables['athlete'].columns['address_street'].drop()
    post_meta.tables['athlete'].columns['address_zip'].drop()
    post_meta.tables['athlete'].columns['date_birth'].drop()
    post_meta.tables['athlete'].columns['disability'].drop()
    post_meta.tables['athlete'].columns['email'].drop()
    post_meta.tables['athlete'].columns['notes'].drop()
    post_meta.tables['athlete'].columns['pace'].drop()
    post_meta.tables['workout'].columns['notes'].drop()
