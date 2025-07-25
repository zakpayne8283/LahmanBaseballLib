import pytest
from db.models.People import People

# Patch the database connection and cursor
class FakeCursor:
    def execute(self, sql, params):
        self.sql = sql
        self.params = params
        self.description = [
            ('ID',), ('playerID',), ('birthYear',), ('birthMonth',), ('birthDay',), 
            ('birthCity',), ('birthCountry',), ('birthState',), 
            ('deathYear',), ('deathMonth',), ('deathDay',), 
            ('deathCountry',), ('deathState',), ('deathCity',), 
            ('nameFirst',), ('nameLast',), ('nameGiven',), 
            ('weight',), ('height',), ('bats',), ('throws',), 
            ('debut',), ('bbrefID',), ('finalGame',), ('retroID',)
        ]
    def fetchall(self):
        return [
            (
                1, 'aardsda01', 1981, 12, 27, 'Denver', 'USA', 'CO',
                None, None, None, None, None, None,
                'David', 'Aardsma', 'David Allan',
                215, 75, 'R', 'R',
                '2004-04-06', 'aardsda01', '2015-08-23', 'aardd001'
            ),
            (
                2, 'aaronha01', 1934, 2, 5, 'Mobile', 'USA', 'AL',
                2021, 1, 22, 'USA', 'GA', 'Atlanta',
                'Hank', 'Aaron', 'Henry Louis',
                180, 72, 'R', 'R',
                '1954-04-13', 'aaronha01', '1976-10-03', 'aaroh101'
            ),
            (
                3, 'aaronto01', 1939, 8, 5, 'Mobile', 'USA', 'AL',
                1984, 8, 16, 'USA', 'GA', 'Atlanta',
                'Tommie', 'Aaron', 'Tommie Lee',
                190, 75, 'R', 'R',
                '1962-04-10', 'aaronto01', '1971-09-26', 'aarot101'
            ),
            (
                4, 'aasedo01', 1954, 9, 8, 'Orange', 'USA', 'CA',
                None, None, None, None, None, None,
                'Don', 'Aase', 'Donald William',
                190, 75, 'R', 'R',
                '1977-07-26', 'aasedo01', '1990-10-03', 'aased001'
            ),
            (
                5, 'abadan01', 1972, 8, 25, 'Palm Beach', 'USA', 'FL',
                None, None, None, None, None, None,
                'Andy', 'Abad', 'Fausto Andres',
                184, 73, 'L', 'L',
                '2001-09-10', 'abadan01', '2006-04-13', 'abada001'
            ),
            (
                6, 'abadfe01', 1985, 12, 17, 'La Romana', 'D.R.', 'La Romana',
                None, None, None, None, None, None,
                'Fernando', 'Abad', 'Fernando Antonio',
                235, 74, 'L', 'L',
                '2010-07-28', 'abadfe01', '2021-10-01', 'abadf001'
            ),
            (
                7, 'abadijo01', 1850, 11, 4, 'Philadelphia', 'USA', 'PA',
                1905, 5, 17, 'USA', 'NJ', 'Pemberton',
                'John', 'Abadie', 'John W.',
                192, 72, 'R', 'R',
                '1875-04-26', 'abadijo01', '1875-06-10', 'abadj101'
            ),
            (
                8, 'abbated01', 1877, 4, 15, 'Latrobe', 'USA', 'PA',
                1957, 1, 6, 'USA', 'FL', 'Fort Lauderdale',
                'Ed', 'Abbaticchio', 'Edward James',
                170, 71, 'R', 'R',
                '1897-09-04', 'abbated01', '1910-09-15', 'abbae101'
            ),
            (
                9, 'abbeybe01', 1869, 11, 11, 'Essex', 'USA', 'VT',
                1962, 6, 11, 'USA', 'VT', 'Colchester',
                'Bert', 'Abbey', 'Bert Wood',
                175, 71, 'R', 'R',
                '1892-06-14', 'abbeybe01', '1896-09-23', 'abbeb101'
            ),
            (
                10, 'abbeych01', 1866, 10, 14, 'Falls City', 'USA', 'NE',
                1926, 4, 27, 'USA', 'CA', 'San Francisco',
                'Charlie', 'Abbey', 'Charles S.',
                169, 68, 'L', 'L',
                '1893-08-16', 'abbeych01', '1897-08-19', 'abbec101'
            )
        ]

class FakeConnection:
    def cursor(self):
        return FakeCursor()

# Running the most basic SELECT statement should return at least 1 row
def test_select(monkeypatch):

    monkeypatch.setattr(People, "get_connection", lambda: FakeConnection())

    results = People.select().execute()
    assert len(results) > 0

# Running a SELECT statement while limiting to 1 should only return one row
def test_select_limit(monkeypatch):
    # TODO: Update the fake data to actually work with querying
    pass
    # monkeypatch.setattr(People, "get_connection", lambda: FakeConnection())

    # results = People.select().limit(1).execute()
    # assert len(results) == 1

# Running a SELECT statement with a specified playerID should return a single player back
def test_select_where(monkeypatch):
    # TODO: Update the fake data to actually work with querying
    pass
    # monkeypatch.setattr(People, "get_connection", lambda: FakeConnection())

    # results = People.select(playerID='aardsda01').execute()

    # assert len(results) == 1
    # assert results[0].playerID == 'aardsda01'
