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
