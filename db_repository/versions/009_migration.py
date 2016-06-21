from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
meauserments = Table('meauserments', pre_meta,
    Column('msm_id', INTEGER, primary_key=True, nullable=False),
    Column('asn_id', INTEGER),
    Column('destination', VARCHAR),
    Column('updated', DATETIME),
)

meauserment = Table('meauserment', post_meta,
    Column('msm_id', Integer, primary_key=True, nullable=False),
    Column('asn_id', Integer),
    Column('destination', String),
    Column('updated', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['meauserments'].drop()
    post_meta.tables['meauserment'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['meauserments'].create()
    post_meta.tables['meauserment'].drop()
