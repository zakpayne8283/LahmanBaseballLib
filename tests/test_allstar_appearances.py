import pytest
from db.models.AllstarApperances import AllstarAppearances

# Patch the database connection and cursor
class FakeCursor:
    def execute(self, sql, params):
        self.sql = sql
        self.params = params
        self.description = [('playerID',), ('yearID',), ('teamID',)]
    def fetchall(self):
        return [
            ('kalinal01', 1957, 0, 'NLS195707090', 'DET', 'AL', 1, 9)
            ]

class FakeConnection:
    def cursor(self):
        return FakeCursor()

# Running the most basic SELECT statement should return at least 1 row
def test_select(monkeypatch):

    monkeypatch.setattr(AllstarAppearances, "get_connection", lambda: FakeConnection())

    results = AllstarAppearances.select().execute()
    assert len(results) > 0

# Running a SELECT statement while limiting to 1 should only return one row
def test_select_limit(monkeypatch):
    monkeypatch.setattr(AllstarAppearances, "get_connection", lambda: FakeConnection())

    results = AllstarAppearances.select().limit(1).execute()
    assert len(results) == 1

# Running a SELECT statement with a specified playerID should return a single player back
def test_select_where(monkeypatch):
    monkeypatch.setattr(AllstarAppearances, "get_connection", lambda: FakeConnection())

    results = AllstarAppearances.select(playerID='kalinal01').execute()

    assert len(results) == 1
    assert results[0].playerID == 'kalinal01'
