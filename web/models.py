from web import db

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
    path_id       = db.Column(db.Integer, primary_key=True)
    origin_asn_id = db.Column(db.Integer, db.ForeignKey(
        'origin_asn.origin_asn_id'))
    path          = db.Column(db.String, unique=True, nullable=False)
    ip_version    = db.Column(db.Integer)

    def __repr__(self):
        return '<Path {}>'.format(self.path)

    def __len__(self):
        return len(self.path_list)

    @property
    def path_list(self):
        return self.path.split(',')

class OriginAsn(db.Model):
    origin_asn_id   = db.Column(
            db.Integer, primary_key = True, autoincrement=False)
    asn_id    = db.Column(db.Integer, db.ForeignKey('asn.asn_id'))
    downstream_asns = db.Column(db.String)
    transit_asns    = db.Column(db.String)
    paths           = db.relationship('Path', backref = 'asn')

    def __repr__(self):
        return '<OriginAsn {}>'.format(self.origin_asn_id)

    @property
    def downstream_asns_list(self):
        return self.downstream_asns.split(',')

    @property
    def transit_asns_list(self):
        return self.transit_asns.split(',')

    @property
    def min_path_len(self):
        return min(map(len, self.paths))

    @property
    def max_path_len(self):
        return min(map(len, self.paths))
