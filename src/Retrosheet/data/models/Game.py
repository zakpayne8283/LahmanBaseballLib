from Retrosheet.data.models.retrosheet_table import RetrosheetTable

class Game(RetrosheetTable):

    game_id = None

    def __init__(self, game_id):
        self.game_id = game_id

    # TODO: Make this a bit better in terms of definition
    #       there's nothing WRONG with the creation, but it could be nicer.
    @classmethod
    def get_table_creation_string(cls):
        creation_sql = cls.table_creation_wrapper("Games").replace("[TABLE_CREATION_SQL]", """
                       CREATE TABLE Games (
                        game_id NVARCHAR(12) PRIMARY KEY
                       );
                       """)
        return creation_sql
    
    # Function to write created game to DB
    def write_to_database(self):
        sql_to_write = f"""
                        INSERT INTO Games (game_id)
                        VALUES ('{self.game_id}');
                       """
        print(sql_to_write)
        cursor = self.get_cursor()
        cursor.execute(sql_to_write)