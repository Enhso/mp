import json
import os

def load_game_data(filepath):
    """
    Loads game data from a JSON file and validates that trigger fragments exist in argument text.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        trigger = item.get('trigger_fragment', '')
        text = item.get('argument_text', '')
        
        if trigger not in text:
            raise ValueError(f"Trigger fragment '{trigger}' not found in argument text for item ID {item.get('id')}")
            
    return data

class GameSession:
    def __init__(self, data):
        self.data = data
        self.current_round_index = 0
        self.scores = []
        self.locked_value = None
        self.total_rounds = len(data)

    def get_current_round_data(self):
        if self.is_game_over():
            return None
        return self.data[self.current_round_index]

    def is_game_over(self):
        return self.current_round_index >= self.total_rounds

    def set_locked_value(self, val):
        self.locked_value = val

    def submit_turn(self, final_value):
        if self.locked_value is None:
            raise ValueError("Locked value must be set before submitting turn.")
        
        current_data = self.get_current_round_data()
        delta = abs(final_value - self.locked_value)
        
        score_entry = {
            'round_id': self.current_round_index,
            'category': current_data.get('category'),
            'delta': delta,
            'technique': current_data.get('technique'),
            'data': current_data
        }
        self.scores.append(score_entry)
        
        self.current_round_index += 1
        self.locked_value = None
