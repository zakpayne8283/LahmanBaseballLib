from db.models.AllstarApperances import AllstarAppearances
from db.models.base_table import TableBase

class People(TableBase):
    def __init__(self, ID, playerID, birthYear, birthMonth, birthDay, birthCity, birthCountry, birthState, deathYear, deathMonth, deathDay,
                 deathCountry, deathState, deathCity, nameFirst, nameLast, nameGiven, weight, height, bats, throws, debut, bbrefID, finalGame, retroID):
        self.ID = ID
        self.playerID = playerID
        self.birthYear = birthYear
        self.birthMonth = birthMonth
        self.birthDay = birthDay
        self.birthCity = birthCity
        self.birthCountry = birthCountry
        self.birthState = birthState
        self.deathYear = deathYear
        self.deathMonth = deathMonth
        self.deathDay = deathDay
        self.deathCountry = deathCountry
        self.deathState = deathState
        self.deathCity = deathCity
        self.nameFirst = nameFirst
        self.nameLast = nameLast
        self.nameGiven = nameGiven
        self.weight = weight
        self.height = height
        self.bats = bats
        self.throws = throws
        self.debut = debut
        self.bbrefID = bbrefID
        self.finalGame = finalGame
        self.retroID = retroID

    # Name of the People table in the DB
    @classmethod
    def table_name(cls):
        return "People"
    
    # Returns the number of allstar apperances for each player
    @classmethod
    def allstar_apperances(cls, player_id=None, year_id=None):
        
        query = People.select("nameFirst", "nameLast").join(AllstarAppearances, "playerID")

        if player_id is not None:
            query.where(playerID=player_id)

        query = (query.aggregate(count=[{"appearances": "*"}])
                      .group_by("playerID", "nameFirst", "nameLast")
                      .order_by(appearances="DESC"))

        return (query.execute())
    
    def full_name(self):
        return self.nameFirst + " " + self.nameLast
    
    def birth_date(self):
        return str(self.birthMonth) + "/" + str(self.birthDay) + "/" + str(self.birthYear)
    
