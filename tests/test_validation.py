import pytest
import json
from game_engine import load_game_data

def test_load_game_data_missing_trigger_fragment(tmp_path):
    # Create an invalid temporary JSON file (trigger_fragment key missing)
    invalid_data = [
        {
            "id": 3,
            "argument_text": "This text does not matter."
            # trigger_fragment is missing
        }
    ]
    d = tmp_path / "missing_trigger_game_data.json"
    d.write_text(json.dumps(invalid_data), encoding='utf-8')
    
    with pytest.raises(ValueError, match="Missing 'trigger_fragment' in item 3"):
        load_game_data(str(d))


def test_load_game_data_missing_category(tmp_path):
    invalid_data = [
        {
            "id": 4,
            "argument_text": "Trigger present",
            "trigger_fragment": "Trigger",
            "technique": "Appeal"
            # category missing
        }
    ]
    d = tmp_path / "missing_category_game_data.json"
    d.write_text(json.dumps(invalid_data), encoding='utf-8')

    with pytest.raises(ValueError, match="Missing or invalid 'category' in item 4"):
        load_game_data(str(d))


def test_load_game_data_missing_technique(tmp_path):
    invalid_data = [
        {
            "id": 5,
            "argument_text": "Trigger present",
            "trigger_fragment": "Trigger",
            "category": "PATHOS"
            # technique missing
        }
    ]
    d = tmp_path / "missing_technique_game_data.json"
    d.write_text(json.dumps(invalid_data), encoding='utf-8')

    with pytest.raises(ValueError, match="Missing or invalid 'technique' in item 5"):
        load_game_data(str(d))
