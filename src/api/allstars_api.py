from db.models.AllstarApperances import AllstarAppearances

# TODO: Be able to use a configuration for a lot of these queries
#       Basically we should be able to do something like top_n_appearances(query_config=query)
#       and that would include things like limits, fields, etc for each query

# TODO: Identify query options
def top_n_appearances(limit: int = 10):
    """
    Returns a list of players whom are in the top N players, by number of allstar appearances.
    """
    from db.models.People import People

    results = (
        AllstarAppearances.select(People.column("nameFirst"), People.column("nameLast"))
                          .join(People, "playerID")
                          .limit(limit)
                          .aggregate(count=[{"allstar_appearances": "*"}])
                          .group_by(People.column("nameFirst"), People.column("nameLast"))
                          .order_by(allstar_appearances="DESC")
                          .execute())
    
    return results

# TODO: Identify query options
def top_n_sub_appearances(limit: int = 10):
    """
    Returns a list of players whom are in the top N players, by number of allstar non-starting appearances.
    """
    from db.models.People import People

    results = (
        AllstarAppearances.select(People.column("nameFirst"), People.column("nameLast"))
                            .join(People, "playerID")
                            .limit(limit)
                            .where(startingPos=None)
                            .aggregate(count=[{"subAppearances": "*"}])
                            .group_by(People.column("nameFirst"), People.column("nameLast"))
                            .order_by(subAppearances="DESC")
                            .execute())
    
    return results

# TODO: Identify query options
def allstars_career_debuts_and_finales(include_as_game_id=False):
    """
    Returns a list of Allstars (by ID) and their first/last names, debuts, final games, and number of appearances
    """
    from db.models.People import People

    # Make sure to unpack your columns! e.g. .select(*columns)
    columns = [
        People.column("playerID"),
        People.column("nameFirst"),
        People.column("nameLast"),
        People.column("debut"),
        People.column("finalGame")
        ]
    
    results = (
        AllstarAppearances.select(*columns)
                          .aggregate(count=[{"allstar_appearances": "*"}])
                          .join(People, "playerID")
                          .group_by(*columns)
                          .execute())
    return results