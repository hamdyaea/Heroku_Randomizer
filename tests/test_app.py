#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: hamdy.aea@protonmail.com
# SPDX-License-Identifier: GPL-3.0-or-later
"""Flask test-client checks, no Dropbox, external HTTP or IP processing."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re

from manage import create_app


def test_random_number_and_counter(tmp_path: Path):
    app = create_app(tmp_path / "visits.sqlite3")
    app.testing = True
    client = app.test_client()
    first = client.get("/")
    second = client.get("/")
    assert first.status_code == second.status_code == 200
    assert b"Executions: <strong>1</strong>" in first.data
    assert b"Executions: <strong>2</strong>" in second.data
    number = re.search(rb'class="number"[^>]*>(\d+)<', second.data)
    assert number is not None and 1 <= int(number.group(1)) <= 1000
    assert b"public ip" not in second.data.lower()


def test_counter_survives_restart(tmp_path: Path):
    db = tmp_path / "counter.sqlite3"
    create_app(db).test_client().get("/")
    assert b"Executions: <strong>2</strong>" in create_app(db).test_client().get("/").data


def test_health_does_not_increment_counter(tmp_path: Path):
    app = create_app(tmp_path / "visits.sqlite3")
    assert app.test_client().get("/health").json == {"status": "ok"}
    assert b"Executions: <strong>1</strong>" in app.test_client().get("/").data


def test_parallel_requests_are_atomic(tmp_path: Path):
    app = create_app(tmp_path / "visits.sqlite3")
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda _: app.test_client().get("/").status_code, range(12)))
    assert results == [200] * 12
    assert b"Executions: <strong>13</strong>" in app.test_client().get("/").data
