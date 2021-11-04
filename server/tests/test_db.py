import sqlite3
import pytest
from kanban.db import initdb_command, get_db


def test_init_db(app):
    runner = app.test_cli_runner()
    result = runner.invoke(initdb_command)
    assert "Initialized the database" in result.output


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)
