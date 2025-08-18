import pytest
from Lahman.db.models.AllstarApperances import AllstarAppearances
from Lahman.db.models.People import People
from Lahman.db.models.query_builder import Query

# Test that the class can instantiate
def test_init():
    # Just using People here because it needs any table
    query = Query(People)

    assert isinstance(query, Query)
    assert len(vars((query))) == 11      # Check number of members
    # This test is more about being mindful for modifying the core Query class

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
    query = Query(AllstarAppearances.select().as_name("allstars")).select("playerID")

    raw_sql = query.build_query()

    assert raw_sql.count("SELECT") == 2
    assert len(query.execute()) > 0

    assert raw_sql.count("AS") == 1

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

    # Test for a HAVING statement being a query
    outer_table_alias = "ASGLeaders"
    query_num_allstars_by_team_by_year = AllstarAppearances.select("teamID").aggregate(count=[{"player_count": "*"}]).where(yearID__var=f"{outer_table_alias}.yearID").group_by("teamID").as_name("teamAllstarAppearancesByYear")
    query_max_asg_players_each_year = Query(query_num_allstars_by_team_by_year).aggregate(max=[{"most_players":"teamAllstarAppearancesByYear.player_count"}])
    query_team_with_most_allstars_by_year = AllstarAppearances.select("yearID", "teamID").aggregate(count=[{"player_count": "*"}]).alias(outer_table_alias).group_by("yearID", "teamID").having(count=[{"=": query_max_asg_players_each_year}])
    
    # TODO: Maybe fix this test up, we're just making sure it outputs results right now...
    assert len(query_team_with_most_allstars_by_year.execute()) > 0

def test_alias():
    table_alias = "needlesslyLongName"
    # Make query
    query = People.select().where(nameFirst="Elly").alias(table_alias)

    # Generate SQL
    raw_sql = query.build_query()

    # query should have needlesslyLongName as the table alias
    assert table_alias in raw_sql

    # Execute Results
    results = query.execute()

    # Make sure the WHERE Statement Works
    assert len(results) == 1

    # Testing a JOIN here
    query = People.select().alias("playerList").where(nameFirst="Elly").join(AllstarAppearances, "playerID")
    results = query.execute()
    assert len(results) == 1