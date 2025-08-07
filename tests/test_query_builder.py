import pytest
from db.models.AllstarApperances import AllstarAppearances
from db.models.People import People
from db.models.query_builder import Query

# Test that the class can instantiate
def test_init():
    # Just using People here because it needs any table
    query = Query(People)

    assert isinstance(query, Query)
    assert len(vars((query))) == 9      # Check number of members

# Test for most basic SELECT statement possible
def test_select():
    query = Query(People)

    # Empty select
    query = query.select()
    # Extract the query
    sql = query.build_query()

    assert "SELECT" in sql
    assert "*" in sql
    assert People.table_name_full() in sql

    query = query.select("nameFirst", "nameLast")
    sql = query.build_query()

    assert "nameFirst" in sql
    assert "nameLast" in sql

def test_select_from_subquery():
    query = Query(AllstarAppearances.select()).select("playerID")

    assert query.build_query().count("SELECT") == 2
    assert len(query.execute()) > 0

def test_where():
    query = Query(People)

    # Empty select
    query = query.select().where(nameFirst="Grover")
    # Extract the query
    sql = query.build_query()

    assert "WHERE" in sql
    assert "nameFirst" in sql
    assert "Grover" in sql

def test_where_subquery():
    query = People.select("playerID", "nameFirst", "nameLast").where(playerID=AllstarAppearances.select("playerID").where(yearID=2024))
    results = query.execute()

    assert len(results) > 0

def test_order_by():
    query = Query(People)

    # Empty select
    query = query.select().order_by(nameFirst="ASC")
    # Extract the query
    sql = query.build_query()

    assert "ORDER BY" in sql
    assert "nameFirst" in sql
    assert "ASC" in sql

def test_limit():
    query = Query(People)

    # Empty select
    query = query.select().limit(10)
    # Extract the query
    sql = query.build_query()

    assert "TOP (10)" in sql

def test_join():
    query = Query(People)

    # Empty select
    query = query.select().join(AllstarAppearances, "playerID")
    # Extract the query
    sql = query.build_query()

    assert "JOIN" in sql
    assert People.table_name_full() in sql
    assert AllstarAppearances.table_name_full() in sql
    assert "ON" in sql
    assert f"{People.table_name_full()}.playerID" in sql
    assert f"{AllstarAppearances.table_name_full()}.playerID" in sql
    assert "=" in sql

def test_group_by():
    query = Query(People)

    # Empty select
    query = query.select().group_by("playerID")
    # Extract the query
    sql = query.build_query()

    assert "playerID FROM" in sql
    assert "GROUP BY playerID" in sql

def test_aggregate():
    query = Query(People)

    # Empty select
    query = query.select().aggregate(count=[{"player": "*"}])
    # Extract the query
    sql = query.build_query()

    assert "COUNT(*)" in sql
    assert "AS player" in sql

def test_having():
    # Query: Allstars with 20 or more appearances
    query = (People.select(f"{People.table_name_full()}.playerID", "nameFirst", "nameLast")
                   .aggregate(count=[{"allstar_appearances": "*"}])
                   .join(AllstarAppearances, "playerID")
                   .group_by(f"{People.table_name_full()}.playerID", "nameFirst", "nameLast")
                   .having(count=[{">": 20}]))
    # Generate SQL strings
    raw_sql = query.build_query()
    # String should have the having statement
    assert "HAVING COUNT(*) > 20" in raw_sql
    # Execute Results
    results = query.execute()
    # Currently there are only 3 players with more than 20 appearances (unlikely to change...)
    assert len(results) == 3