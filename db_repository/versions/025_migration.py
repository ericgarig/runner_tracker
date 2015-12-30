from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
athlete = Table('athlete', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name_first', String(length=64)),
    Column('name_last', String(length=64)),
    Column('phone_number', String(length=10)),
    Column('email', String(length=64)),
    Column('date_birth', Date),
    Column('address_street', String(length=64)),
    Column('address_city', String(length=64)),
    Column('address_state', String(length=2)),
    Column('address_zip', String(length=5)),
    Column('ice_name', String(length=64)),
    Column('ice_phone', String(length=10)),
    Column('disability', String(length=64)),
    Column('pace', Float),
    Column('shirt_size', String(length=5)),
    Column('note', Text),
    Column('is_handcrank', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['athlete'].columns['shirt_size'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['athlete'].columns['shirt_size'].drop()
