from db.models.base_table import TableBase

#TODO: Fix all instances where I've mistakenly spelled it apperances
class AllstarAppearances(TableBase):
    
    # Constructor - used for returning instances of AllstarAppearances in super().select()
    def __init__(self, playerID=None, gameNum=None, gameID=None, yearID=None, teamID=None, lgID=None, GP=None, startingPos=None):
        self.playerID = playerID
        self.gameNum = gameNum
        self.gameID = gameID
        self.yearID = yearID
        self.teamID = teamID
        self.lgID = lgID
        self.GP = GP
        self.startingPos = startingPos

    @classmethod
    def table_name(cls):
        return "AllstarFull"

    @classmethod
    def most_non_starting_appearances(cls):
        from db.models.People import People

        nameFirst = f"{People.table_name_full()}.nameFirst"
        nameLast = f"{People.table_name_full()}.nameLast"

        results = (
            AllstarAppearances.select(nameFirst, nameLast)
                              .join(People, "playerID")
                              .limit(10)
                              .where(startingPos=None)
                              .aggregate(count=[{"subAppearances": "*"}])
                              .group_by(nameFirst, nameLast)
                              .order_by(subAppearances="DESC")
                              .execute())
        
        return results