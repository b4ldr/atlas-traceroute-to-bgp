from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
asn = Table('asn', post_meta,
    Column('asn_id', Integer, primary_key=True, nullable=False),
    Column('downstream_asns', String),
    Column('transit_asns', String),
)

msm = Table('msm', post_meta,
    Column('msm_id', Integer, primary_key=True, nullable=False),
    Column('prefix_id', Integer),
    Column('updated', DateTime),
)

path = Table('path', post_meta,
    Column('path_id', Integer, primary_key=True, nullable=False),
    Column('asn_id', Integer),
    Column('path', String, nullable=False),
)

prefix = Table('prefix', post_meta,
    Column('prefix_id', Integer, primary_key=True, nullable=False),
    Column('prefix', String, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['asn'].create()
    post_meta.tables['msm'].create()
    post_meta.tables['path'].create()
    post_meta.tables['prefix'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['asn'].drop()
    post_meta.tables['msm'].drop()
    post_meta.tables['path'].drop()
    post_meta.tables['prefix'].drop()
