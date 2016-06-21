from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
origin_asn = Table('origin_asn', post_meta,
    Column('origin_asn_id', Integer, primary_key=True, nullable=False),
    Column('asn_id', Integer),
    Column('downstream_asns', String),
    Column('transit_asns', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['origin_asn'].columns['asn_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['origin_asn'].columns['asn_id'].drop()
