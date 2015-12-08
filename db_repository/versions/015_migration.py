from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
athlete = Table('athlete', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name_first', VARCHAR(length=64)),
    Column('name_last', VARCHAR(length=64)),
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
    Column('pace', FLOAT),
    Column('note', TEXT),
    Column('name_nick', VARCHAR(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['athlete'].columns['name_nick'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['athlete'].columns['name_nick'].create()
