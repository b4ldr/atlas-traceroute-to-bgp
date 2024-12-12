# atlas-traceroute-to-bgp
an app to reduce atlas traceroute measurements to bgp hop counts

The following should get one started

```bash
git clone https://github.com/b4ldr/atlas-traceroute-to-bgp/
pip3 install Flask Flask-Bootstrap Flask-SQLAlchemy alembic PrettyTable ripe.atlas.sagan ripe.atlas.cousteau pyasn cymruwhois ipy
flask --app web shell
>>> from web.models import db
>>> db.create_all()
flask --app web run
```

after this you can connect to http://localhost:5000; add an ASN then ADD a traceroute measuerment ID.
