from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
msm = Table('msm', pre_meta,
    Column('msm_id', INTEGER, primary_key=True, nullable=False),
    Column('prefix_id', INTEGER),
    Column('updated', DATETIME),
)

prefix = Table('prefix', pre_meta,
    Column('prefix_id', INTEGER, primary_key=True, nullable=False),
    Column('prefix', VARCHAR, nullable=False),
    Column('asn_id', INTEGER),
)

meauserments = Table('meauserments', post_meta,
    Column('msm_id', Integer, primary_key=True, nullable=False),
    Column('asn_id', Integer),
    Column('destination', String),
    Column('updated', DateTime),
)

path = Table('path', post_meta,
    Column('path_id', Integer, primary_key=True, nullable=False),
    Column('origin_asn_id', Integer),
    Column('path', String, nullable=False),
    Column('ip_version', Integer),
)

asn = Table('asn', pre_meta,
    Column('asn_id', INTEGER, primary_key=True, nullable=False),
    Column('ip_version', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['msm'].drop()
    pre_meta.tables['prefix'].drop()
    post_meta.tables['meauserments'].create()
    post_meta.tables['path'].columns['ip_version'].create()
    pre_meta.tables['asn'].columns['ip_version'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['msm'].create()
    pre_meta.tables['prefix'].create()
    post_meta.tables['meauserments'].drop()
    post_meta.tables['path'].columns['ip_version'].drop()
    pre_meta.tables['asn'].columns['ip_version'].create()
