import pytest
import json
import os
from game_engine import load_game_data, GameSession

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

def test_game_session_initialization():
    data = [
        {"id": 1, "text": "Round 1"},
        {"id": 2, "text": "Round 2"}
    ]
    session = GameSession(data)
    
    assert session.current_round_index == 0
    assert session.scores == []
    assert session.locked_value is None
    assert session.total_rounds == 2
    assert not session.is_game_over()
    
    round_data = session.get_current_round_data()
    assert round_data == data[0]

def test_game_session_scoring():
    data = [
        {
            "id": 1, 
            "text": "Round 1", 
            "category": "PATHOS", 
            "technique": "Appeal to Fear"
        },
        {
            "id": 2, 
            "text": "Round 2", 
            "category": "LOGOS", 
            "technique": "Appeal to Logic"
        }
    ]
    session = GameSession(data)
    
    # Round 1
    session.set_locked_value(50)
    session.submit_turn(70)
    
    assert len(session.scores) == 1
    score = session.scores[0]
    assert score['round_id'] == 0
    assert score['delta'] == 20  # abs(70 - 50)
    assert score['category'] == "PATHOS"
    assert score['technique'] == "Appeal to Fear"
    
    assert session.current_round_index == 1
    assert session.locked_value is None
    
    # Round 2
    session.set_locked_value(30)
    session.submit_turn(25)
    
    assert len(session.scores) == 2
    score = session.scores[1]
    assert score['round_id'] == 1
    assert score['delta'] == 5   # abs(25 - 30)
    
    assert session.current_round_index == 2
    assert session.is_game_over()
