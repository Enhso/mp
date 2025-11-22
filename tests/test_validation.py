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
