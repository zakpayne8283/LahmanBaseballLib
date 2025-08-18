import pytest
from Lahman.db.models.AllstarApperances import AllstarAppearances
from Lahman.db.models.People import People

# Test table_name & table_name_full
def test_table_name():
    assert AllstarAppearances.table_name() == "AllstarFull"
    assert AllstarAppearances.table_name_full() == "dbo.AllstarFull"

# Running the most basic SELECT statement should return at least 1 row
def test_select():

    results = AllstarAppearances.select().execute()
    assert len(results) > 0

# Running a SELECT statement with a specified playerID should return a single player back
def test_where():

    # Testing this with ID=jacksbo01 ==> Bo Jackson will not play another all star game (although I bet he still could)
    results = AllstarAppearances.select().where(playerID='jacksbo01').execute()

    assert len(results) == 1
    assert results[0].playerID == 'jacksbo01'

    results = AllstarAppearances.select().where(yearID__gt=2000).execute()
    assert len(results) > 0

# ORDER BY should return the lowest year
def test_order_by():

    results = AllstarAppearances.select().order_by(yearID="ASC").execute()
    assert results[0].yearID == 1933

# Running a SELECT statement while limiting to 1 should only return one row
def test_select_limit():
    results = AllstarAppearances.select().limit(1).execute()
    assert len(results) == 1

# Joining on People should have access to each player's first and last names
def test_join():
    # Join People table on playerID
    # Also just limit to 1, so it's easy to check
    results = AllstarAppearances.select().limit(1).join(People, "playerID").execute()

    assert results[0].nameFirst == "Hank"   # Shouldn't be Hank, should be Henry...
    assert results[0].nameLast == "Aaron"

def test_group_by():
    results = AllstarAppearances.select().group_by("playerID").execute()

    assert len(results) == 2017 # TODO: Keep an eye on this, subject to change

def test_aggregate():
    results = AllstarAppearances.select().aggregate(count=[{"playerCount":"*"}]).group_by("yearID").order_by(yearID="DESC").execute()

    assert len(results) == 91   # TODO: Keep an eye on this, subject to change
    assert results[0].playerCount == 76 # 76 players in the 2024 AS Game
