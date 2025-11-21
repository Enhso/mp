import streamlit as st
import os
from annotated_text import annotated_text
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
    
    if 'step' not in st.session_state:
        st.session_state.step = 'bet'

def main():
    st.set_page_config(page_title="MindPatch Prototype", layout="centered")
    
    initialize_game()
    
    engine = st.session_state.engine
    
    st.title("MindPatch Prototype")
    
    # Progress Bar
    if engine.total_rounds > 0:
        progress = engine.current_round_index / engine.total_rounds
        st.progress(progress)
    
    # Game Logic
    current_data = engine.get_current_round_data()
    
    if current_data and st.session_state.step == 'bet':
        st.header(f"Claim: {current_data['claim']}")
        
        slider_val = st.slider("Your Stance", 0, 100, 50)
        
        if st.button("🔒 Lock In"):
            engine.set_locked_value(slider_val)
            st.session_state.step = 'attack'
            st.rerun()

    elif current_data and st.session_state.step == 'attack':
        st.header(f"Claim: {current_data['claim']}")
        st.info(f"🔒 You locked in at: {engine.locked_value}")
        
        st.warning(current_data['argument_text'])
        
        new_slider_val = st.slider("Does this change your view?", 0, 100, engine.locked_value)
        
        if st.button("Submit Final Position"):
            engine.submit_turn(new_slider_val)
            
            if engine.is_game_over():
                st.session_state.step = 'finished'
            else:
                st.session_state.step = 'bet'
            st.rerun()

    elif st.session_state.step == 'finished':
        st.success("Game Over! Here is your X-Ray Analysis:")
        
        results = engine.get_results_summary()
        if results['weakness']:
            st.error(f"⚠️ Your Primary Weakness: {results['weakness']}")
        
        st.divider()
        
        for score in engine.scores:
            # Only show analysis if the user was swayed significantly (e.g., > 10 points)
            if score['delta'] > 10:
                st.subheader(f"Round {score['round_id'] + 1}: {score['category']}")
                st.write(f"You were swayed by **{score['delta']} points**.")
                
                data = score['data']
                trigger = data['trigger_fragment']
                full_text = data['argument_text']
                
                # Split text to highlight trigger
                parts = full_text.split(trigger)
                
                if len(parts) >= 2:
                    annotated_text(
                        parts[0],
                        (trigger, score['technique'], "#faa"),
                        parts[1]
                    )
                else:
                    st.write(full_text)
                
                with st.expander("🛡️ See Antidote"):
                    st.info(data['antidote'])
                
                st.divider()
        
        if st.button("Restart Game"):
            st.session_state.clear()
            st.rerun()

    elif current_data is None:
        # Fallback if something goes wrong with state
        st.session_state.step = 'finished'
        st.rerun()

if __name__ == "__main__":
    main()
