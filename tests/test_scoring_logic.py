import pytest
from game_engine import GameSession

def test_backfire_effect_scoring():
    """
    Test that the backfire effect (moving against the argument) results in a negative score
    and is not classified as a weakness compared to a smaller positive sway.
    """
    data = [
        {"id": 1, "category": "Category A (Backfire)", "technique": "T1"},
        {"id": 2, "category": "Category B (Small Sway)", "technique": "T2"}
    ]
    session = GameSession(data)
    
    # Round 1: Backfire
    # User locks in 80, moves to 50.
    # Expected Delta: 50 - 80 = -30
    session.set_locked_value(80)
    session.submit_turn(50)
    
    assert session.scores[0]['delta'] == -30
    
    # Round 2: Small Sway
    # User locks in 50, moves to 60.
    # Expected Delta: 60 - 50 = +10
    session.set_locked_value(50)
    session.submit_turn(60)
    
    assert session.scores[1]['delta'] == 10
    
    # Check Results
    summary = session.get_results_summary()
    
    # Weakness should be Category B because +10 > -30
    assert summary['weakness'] == "Category B (Small Sway)"
    assert summary['stats']["Category A (Backfire)"] == -30
    assert summary['stats']["Category B (Small Sway)"] == 10
