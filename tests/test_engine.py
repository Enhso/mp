import pytest
import json
import os
from game_engine import load_game_data

def test_load_game_data_valid(tmp_path):
    # Create a valid temporary JSON file
    valid_data = [
        {
            "id": 1,
            "argument_text": "This is a sample argument text with a trigger.",
            "trigger_fragment": "trigger"
        }
    ]
    d = tmp_path / "valid_game_data.json"
    d.write_text(json.dumps(valid_data), encoding='utf-8')
    
    loaded_data = load_game_data(str(d))
    assert len(loaded_data) == 1
    assert loaded_data[0]['id'] == 1

def test_load_game_data_invalid_fragment(tmp_path):
    # Create an invalid temporary JSON file (fragment missing)
    invalid_data = [
        {
            "id": 2,
            "argument_text": "This text does not contain the fragment.",
            "trigger_fragment": "missing fragment"
        }
    ]
    d = tmp_path / "invalid_game_data.json"
    d.write_text(json.dumps(invalid_data), encoding='utf-8')
    
    with pytest.raises(ValueError, match="Trigger fragment 'missing fragment' not found"):
        load_game_data(str(d))
