# Randomizatorh — Privacy-Safe Flask Demo

Developer: Hamdy Abou El Anein
Contact: hamdy.aea@protonmail.com
License: GNU GPL v3 (see LICENSE).

This project modernizes a historic Heroku Flask experiment. The original
version downloaded and deleted Dropbox files on every visit and submitted
visitors' IP addresses to an external geolocation service. These operations
have been removed.

The current application uses Python's cryptographic random generator and a
local SQLite counter. It does not collect IP addresses, contact Dropbox,
call geolocation APIs or require secrets. Existing `visitors.csv` and
`countrylist.txt` are retained as historical files but are **not read**.
No remote Dropbox data is deleted or migrated by this modernization.

## Run locally

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python manage.py
```

Open http://127.0.0.1:5000. The SQLite database is stored in Flask's
`instance/` directory by default. Set `RANDOMIZER_DATABASE` to use
another database location.

For a production WSGI server, use `gunicorn manage:app` behind a
properly configured reverse proxy. Do not use the Flask development server
in production. Deployment is intentionally not performed here.

The original application is preserved in Git branch `old`.
