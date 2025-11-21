import streamlit as st
import os
from game_engine import load_game_data, GameSession

# Constants
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'game_data.json')

def initialize_game():
    if 'engine' not in st.session_state:
        try:
            data = load_game_data(DATA_FILE)
            st.session_state.engine = GameSession(data)
        except Exception as e:
            st.error(f"Failed to load game data: {e}")
            st.stop()

def main():
    st.set_page_config(page_title="MindPatch Prototype", layout="centered")
    
    initialize_game()
    
    engine = st.session_state.engine
    
    st.title("MindPatch Prototype")
    
    # Progress Bar
    if engine.total_rounds > 0:
        progress = engine.current_round_index / engine.total_rounds
        st.progress(progress)
    
    # Debug Output
    st.write("Current Round Data (Debug):")
    st.write(engine.get_current_round_data())

if __name__ == "__main__":
    main()
