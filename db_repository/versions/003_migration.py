from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
destination_asn = Table('destination_asn', pre_meta,
    Column('destination_asn_id', INTEGER, primary_key=True, nullable=False),
)

asn = Table('asn', post_meta,
    Column('asn_id', Integer, primary_key=True, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['destination_asn'].drop()
    post_meta.tables['asn'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['destination_asn'].create()
    post_meta.tables['asn'].drop()
