import pytest

# API imports
from api import allstars_api

def test_allstar_appearances():
    as_appearances = allstars_api.top_n_appearances()
    assert len(as_appearances) == 10

def test_allstar_sub_appearances():
    as_appearances = allstars_api.top_n_sub_appearances()

    assert len(as_appearances) == 10

def test_allstars_career_debuts_and_finales():
    as_appearances = allstars_api.allstars_career_debuts_and_finales()

    assert len(as_appearances) > 0