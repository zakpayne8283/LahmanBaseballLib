from Lahman.db.models.lahman_table import LahmanTable

#TODO: Fix all instances where I've mistakenly spelled it apperances
class AllstarAppearances(LahmanTable):
    
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