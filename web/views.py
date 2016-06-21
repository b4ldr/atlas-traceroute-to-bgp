from logging import debug, error, warning, info
from IPy import IP
from datetime import datetime
from web import app, PYASN_FILE, models, db
from trace2bgp.atlas import Asn, Asns
from trace2bgp.utils import Lookup, get_sagan_objects, get_cousteau_object
from ripe.atlas.cousteau import Measurement
from flask import render_template, redirect, url_for, request, flash, session

@app.route('/')
def index():
    asns = models.Asn.query.order_by(models.Asn.asn_id).all()
    return render_template('index.html', asns=asns)

@app.route('/msm/<int:msm_id>')
def msm_id(msm_id):
    asns = Asns(msm_id, PYASN_FILE)
    return render_template('msm.html', asns=asns.asns)

def check_msm(msm_id, asn):
    try:
        msm_meta = Measurement(id=msm_id)
    except Exception as e:
        debug('{}'.format(e))
        flash('{}'.format(e), 'error')
        return False
        
    if msm_meta.type != 'traceroute':
        flash('measurement {} is {} not traceroute'.format(
            msm_id, msm_meta.type), 'error')
        return False
    msm_meta.target_asn = Lookup().lookup(msm_meta.target_ip)
    if int(msm_meta.target_asn) != int(asn):
        flash('measurement {} target is in AS{} not AS{}'.format(
            msm_id, msm_meta.target_asn, asn), 'error')
        return False
    return msm_meta

def update_msm(asn_model, msm_meta):
    measurement_model = models.Meauserment.query.filter_by(
            msm_id = msm_meta.id).first()
    if not measurement_model:
        measurement_model = models.Meauserment(
                msm_id=msm_meta.id, destination=msm_meta.target_ip, asn=asn_model)
        db.session.add(measurement_model)
    measurement_model.updated = datetime.now()

def update_origin_asn(asn_model, asns):
    for asn in asns.asns:
        orig_asn_model = models.OriginAsn.query.filter_by(
                origin_asn_id=asn.id).first()
        if not orig_asn_model:
            orig_asn_model = models.OriginAsn(origin_asn_id=asn.id, asn=asn_model)
            db.session.add(orig_asn_model)
        orig_asn_model.downstream_asns = ', '.join(asn.downstream_asns)
        orig_asn_model.transit_asns    = ', '.join(asn.transit_asns)
        for path in asn.paths:
            path_str = ', '.join(path)
            path_model = models.Path.query.filter_by(
                    asn=orig_asn_model, path=path_str).first()
            if not path_model:
                path_model = models.Path(asn=orig_asn_model, path=path_str)
                db.session.add(path_model)

@app.route('/asn/<int:asn>', methods=['GET', 'POST'])
def asn(asn):
    asn_model = models.Asn.query.filter_by(asn_id=asn).first()
    if not asn_model:
        asn_model = models.Asn(asn_id = asn)
        db.session.add(asn_model)
    if request.method == 'POST':
        msm_id = request.form['msm_id']
        msm_meta = check_msm(msm_id, asn)
        if msm_meta:
            cousteau_object = get_cousteau_object(msm_id)
            sagan_object    = get_sagan_objects(cousteau_object)
            asns            = Asns(sagan_object, PYASN_FILE)
            flash('Atlas Measurement added: {}'.format(msm_id)) 
            update_msm(asn_model, msm_meta)
            update_origin_asn(asn_model, asns)

    db.session.commit()
    return render_template('asn.html', asn=asn_model)

@app.route('/origin_asn/<int:asn>')
def origin_asn(asn):
    asn_model = models.OriginAsn.query.filter_by(origin_asn_id=asn).first()
    if not asn_model:
        flash('AS{} not in DB')
    return render_template('origin_asn.html', asn=asn_model)
