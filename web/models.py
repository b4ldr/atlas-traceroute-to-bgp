from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from web import app

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)

paths_join = db.Table('paths_join',
        db.Column('path_id', db.Integer, db.ForeignKey('path.path_id')),
        db.Column('origin_asn_id', db.Integer, db.ForeignKey('origin_asn.origin_asn_id')))

class Meauserment(db.Model):
    msm_id      = db.Column(db.Integer, primary_key=True, autoincrement=False)
    asn_id      = db.Column(db.Integer, db.ForeignKey('asn.asn_id'))
    destination = db.Column(db.String)
    updated     = db.Column(db.DateTime)

    def __repr__(self):
        return '<Msm {}>'.format(self.msm_id)


class Asn(db.Model):
    asn_id       = db.Column(db.Integer, primary_key=True, autoincrement=False)
    origin_asns  = db.relationship('OriginAsn', backref='asn', lazy='dynamic')
    meauserments = db.relationship('Meauserment', backref='asn', lazy='dynamic')

    def __repr__(self):
        return '<Asn {}>'.format(self.asn_id)

class Path(db.Model):
    path_id     = db.Column(db.Integer, primary_key=True)
    origin_asns = db.relationship(
        'OriginAsn', secondary=paths_join, backref=db.backref('path'))
    path          = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<Path {}>'.format(self.path)

    def __len__(self):
        return len(self.path_list)

    @property
    def path_list(self):
        if self.path:
            return self.path.split(',')
        return []

class OriginAsn(db.Model):
    origin_asn_id   = db.Column(db.Integer, primary_key=True)
    origin_asn      = db.Column(db.Integer)
    asn_id          = db.Column(db.Integer, db.ForeignKey('asn.asn_id'))
    downstream_asns = db.Column(db.String)
    transit_asns    = db.Column(db.String)
    paths           = db.relationship(
        'Path', secondary=paths_join, backref=db.backref('origin_asn'))
    ip_version      = db.Column(db.Integer)

    def __repr__(self):
        return '<OriginAsn {}>'.format(self.origin_asn_id)

    @property
    def downstream_asns_list(self):
        if self.downstream_asns:
            return self.downstream_asns.split(',')
        return []


    @property
    def transit_asns_list(self):
        if self.transit_asns:
            return self.transit_asns.split(',')
        return []

    @property
    def min_path_len(self):
        return min(map(len, self.paths))

    @property
    def max_path_len(self):
        return min(map(len, self.paths))
