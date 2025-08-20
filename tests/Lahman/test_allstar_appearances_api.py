import pytest

# API imports
from Lahman.api import allstars_api

def test_allstar_appearances():
    as_appearances = allstars_api.top_n_appearances()
    assert len(as_appearances) == 10

def test_allstar_sub_appearances():
    as_appearances = allstars_api.top_n_sub_appearances()

    assert len(as_appearances) == 10

def test_allstars_career_debuts_and_finales():
    as_appearances = allstars_api.allstars_career_debuts_and_finales()

    assert len(as_appearances) > 0

def test_allstars_starters_information():
    as_starters = allstars_api.allstars_starters_information(starting_position=1)

    assert len(as_starters) > 0