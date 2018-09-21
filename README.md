# atlas-traceroute-to-bgp
an app to reduce atlas traceroute measurements to bgp hop counts

The following should get one started

```bash
git clone https://github.com/b4ldr/atlas-traceroute-to-bgp/
pip install Flask Flask-Bootstrap Flask-SQLAlchemy SQLAlchemy-migrate PrettyTable ripe.atlas.sagan ripe.atlas.cousteau pyasn cymruwhois ipy
python db_create.py
python run.py
```

after this you can connect to http://localhost:5000; add an ASN then ADD a traceroute measuerment ID.
