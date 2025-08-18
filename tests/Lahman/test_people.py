import pytest
from Lahman.db.models.People import People

# TODO: Implement the core SQL statements for People too?
# Unsure it's needed, they're being covered by other tests.
# Might be nice to have just because if there are any unexpected changes to the DB they can be caught

# Running the most basic SELECT statement should return at least 1 row
def test_select():
    people = People.select().execute()

    assert len(people) > 0

# Running a SELECT statement while limiting to 1 should only return one row
def test_limit():
    pass

# Running a SELECT statement with a specified playerID should return a single player back
def test_where():
    pass

def test_full_name():
    player = People.select().where(playerID="aaronha01").execute()

    assert len(player) == 1
    assert player[0].full_name() == "Hank Aaron"

def test_birth_date():
    player = People.select().where(playerID="aaronha01").execute()

    assert len(player) == 1
    assert player[0].birth_date() == "2/5/1934"

# TODO: Move these? These might just be good to move to the allstar API tests.
# def test_allstar_apperances():

#     as_apperances = People.allstar_apperances()
#     assert len(as_apperances) == 2017 #TODO: Keep an eye on this, subject to change

#     as_apperances = People.allstar_apperances(limit=10)
#     assert len(as_apperances) == 10

#     as_apperances = People.allstar_apperances(player_id="aaronha01")
#     assert len(as_apperances) == 1

