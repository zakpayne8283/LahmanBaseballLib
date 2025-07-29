# Project Information
LahmanBaseballLib is a project looking to create an easy python wrapper for interacting with the [Lahman Baseball Database](https://sabr.org/lahman-database/) (Credit: SABR)

## Todo
- Create/Update documentation for:
    - `Query()` methods
    - Charts available
- Create classes for each remaining DB Table
    - Appearances
    - AwardsManagers
    - AwardsPlayers
    - AwardsShareManagers
    - AwardsSharePlayers
    - Batting
    - BattingPost
    - CollegePlaying
    - Fielding
    - FieldingOF
    - FieldingOFsplit
    - FieldingPost
    - HallOfFame
    - HomeGames
    - Managers
    - ManagersHalf
    - Parks
    - Pitching
    - PitchingPost
    - Salaries
    - Schools
    - SeriesPost
    - Teams
    - TeamsFranchises
    - TeamsHalf

## Ideas
- Script for importing data automatically
    - Maybe just handle this in `cli/main.py`?
    - Check for running SQLExpress Instance
    - Check `.env` file for expected DB info
## Completed
- Define a basic data wrapper for each table
    - AllstarFull
    - People