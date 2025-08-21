class AtBatResultsParser:

    """
    Examples (brackets are not present in data)
    play,1,0,duraj001,00,X,[6/P78S]
    play,1,0,dever001,32,CBBBS,[NP]
    play,1,0,dever001,32,CBBBS.*B,[W]
    play,1,0,stort001,01,CX,[8/F89]
    play,1,0,yoshm002,20,BB,[NP]
    play,1,0,yoshm002,32,BB.BCS>C,[K]
    """

    def __init__(self, results_string):
        # The string we're seeing (see examples above)
        self.at_bat_results_string = results_string

        # No play - skip
        self.no_play = False

        # Parse on initialization
        self.parse()

    def parse(self):

        # First check if NP (no play)
        #   if it's NP, we can skip everything else
        if self.at_bat_results_string.upper() == "NP":
            self.no_play = True
            return
        
        # Now break down by possible results...

    def is_no_play(self):
        return self.no_play