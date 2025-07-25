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


    @classmethod
    def table_name(cls):
        return "People"
    
    def full_name(self):
        return self.nameFirst + " " + self.nameLast
    
    def birth_date(self):
        return str(self.birthMonth) + "/" + str(self.birthDay) + "/" + str(self.birthYear)