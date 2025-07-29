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

    #TODO: Find a way to move this to People instead
    #TODO: Currently held back by limitations on .where()
    @classmethod
    def most_non_starting_appearances(cls):
        from db.models.People import People

        results = (
            AllstarAppearances.select(People.column("nameFirst"), People.column("nameLast"))
                              .join(People, "playerID")
                              .limit(10)
                              .where(startingPos=None)
                              .aggregate(count=[{"subAppearances": "*"}])
                              .group_by(People.column("nameFirst"), People.column("nameLast"))
                              .order_by(subAppearances="DESC")
                              .execute())
        
        return results