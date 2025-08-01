import pytest
from db.models.AllstarApperances import AllstarAppearances
from db.models.People import People
from db.models.query_builder import Query

# Test that the class can instantiate
def test_init():
    # Just using People here because it needs any table
    query = Query(People)

    assert isinstance(query, Query)
    assert len(vars((query))) == 8      # Check number of members

# Test for most basic SELECT statement possible
def test_select():
    query = Query(People)

    # Empty select
    query = query.select()
    # Extract the query
    sql = query.build_query()[0]

    assert "SELECT" in sql
    assert "*" in sql
    assert People.table_name_full() in sql

    query = query.select("nameFirst", "nameLast")
    sql = query.build_query()[0]

    assert "nameFirst" in sql
    assert "nameLast" in sql

def test_select_from_subquery():
    query = Query(AllstarAppearances.select()).select("playerID")

    assert query.build_query()[0].count("SELECT") == 2
    assert len(query.execute()) > 0

def test_where():
    query = Query(People)

    # Empty select
    query = query.select().where(nameFirst="Grover")
    # Extract the query
    sql, params = query.build_query()

    assert "WHERE" in sql
    assert "nameFirst" in sql
    assert "Grover" in params

def test_order_by():
    query = Query(People)

    # Empty select
    query = query.select().order_by(nameFirst="ASC")
    # Extract the query
    sql = query.build_query()[0]

    assert "ORDER BY" in sql
    assert "nameFirst" in sql
    assert "ASC" in sql

def test_limit():
    query = Query(People)

    # Empty select
    query = query.select().limit(10)
    # Extract the query
    sql = query.build_query()[0]

    assert "TOP (10)" in sql

def test_join():
    query = Query(People)

    # Empty select
    query = query.select().join(AllstarAppearances, "playerID")
    # Extract the query
    sql = query.build_query()[0]

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
    sql = query.build_query()[0]

    assert "playerID FROM" in sql
    assert "GROUP BY playerID" in sql

def test_aggregate():
    query = Query(People)

    # Empty select
    query = query.select().aggregate(count=[{"player": "*"}])
    # Extract the query
    sql = query.build_query()[0]

    assert "COUNT(*)" in sql
    assert "AS player" in sql
