import pytest
from db.models.AllstarApperances import AllstarAppearances

# Running the most basic SELECT statement should return at least 1 row
def test_select():

    results = AllstarAppearances.select().execute()
    assert len(results) > 0

# Running a SELECT statement while limiting to 1 should only return one row
def test_select_limit():

    results = AllstarAppearances.select().limit(1).execute()
    assert len(results) == 1

# Running a SELECT statement with a specified playerID should return a single player back
def test_select_where():

    # Testing this with ID=jacksbo01 ==> Bo Jackson will not play another all star game (although I bet he still could)

    results = AllstarAppearances.select().where(playerID='jacksbo01').execute()

    assert len(results) == 1
    assert results[0].playerID == 'jacksbo01'
