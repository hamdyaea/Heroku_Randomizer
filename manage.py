#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: hamdy.aea@protonmail.com
# SPDX-License-Identifier: GPL-3.0-or-later
"""Privacy-preserving Flask random-number demo; no Dropbox or IP lookups."""
from __future__ import annotations

import os
from pathlib import Path
import secrets
import sqlite3

from flask import Flask, render_template


def create_app(database_path: str | Path | None = None) -> Flask:
    app = Flask(__name__)
    if database_path is None:
        database_path = os.environ.get("RANDOMIZER_DATABASE")
    database = Path(database_path) if database_path else Path(app.instance_path) / "visits.sqlite3"

    def next_count() -> int:
        database.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(database, timeout=10) as connection:
            connection.execute("CREATE TABLE IF NOT EXISTS counters (name TEXT PRIMARY KEY, value INTEGER NOT NULL)")
            connection.execute(
                "INSERT INTO counters (name, value) VALUES ('visits', 1) "
                "ON CONFLICT(name) DO UPDATE SET value=value+1"
            )
            return int(connection.execute("SELECT value FROM counters WHERE name='visits'").fetchone()[0])

    @app.get("/")
    def index():
        return render_template("index.html", random_number=secrets.randbelow(1000) + 1,
                               counter=next_count())

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
