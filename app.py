import streamlit as st
import os
import re
import plotly.express as px
import pandas as pd
from annotated_text import annotated_text
from game_engine import load_game_data, GameSession

# Constants
DATA_FILE = os.environ.get('GAME_DATA_FILE', os.path.join(os.path.dirname(__file__), 'data', 'game_data.json'))

def initialize_game():
    if 'engine' not in st.session_state:
        if not os.path.exists(DATA_FILE):
            st.error(f"Game data file not found at: {DATA_FILE}. Please ensure the file exists or set GAME_DATA_FILE environment variable.")
            st.stop()

        try:
            data = load_game_data(DATA_FILE)
            st.session_state.engine = GameSession(data)
        except Exception as e:
            st.error(f"Failed to load game data: {e}")
            st.stop()
    
    if 'step' not in st.session_state:
        st.session_state.step = 'intro'

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
    
    if st.session_state.step == 'intro':
        st.markdown("""
        ### Welcome to MindPatch 🧷
        
        **Can you be manipulated?**
        
        MindPatch is a cognitive immunology training tool. In this simulation, we will test your resistance to persuasive rhetoric.
        
        **How it works:**
        1. You'll see a controversial claim.
        2. You'll take a stance (0-100%).
        3. You'll be exposed to a counter-argument designed to exploit specific cognitive vulnerabilities.
        4. You'll decide if your stance has shifted.
        
        At the end, we'll analyze which rhetorical techniques you are most susceptible to.
        """)
        
        if st.button("Start Simulation", type="primary"):
            st.session_state.step = 'bet'
            st.rerun()

    elif current_data and st.session_state.step == 'bet':
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
            st.session_state.step = 'feedback'
            st.rerun()

    elif st.session_state.step == 'feedback':
        last_score = engine.scores[-1]
        delta = last_score['delta']
        data = last_score['data']
        
        st.header("Round Feedback")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Shift in Stance", f"{delta}")
        
        with col2:
            if delta < 10:
                st.success("🛡️ **Resilient!** You held your ground.")
            elif delta < 30:
                st.warning("⚠️ **Wavering.** You were slightly influenced.")
            else:
                st.error("🚨 **Vulnerable!** You were significantly swayed.")
        
        st.divider()
        
        # Reflection
        st.text_area("Reflection: Why did this work (or not work) on you?", placeholder="I felt that...")
        
        if st.button("Next Round"):
            if engine.is_game_over():
                st.session_state.step = 'finished'
            else:
                st.session_state.step = 'bet'
            st.rerun()

    elif st.session_state.step == 'finished':
        st.success("Game Over! Here is your X-Ray Analysis:")
        
        results = engine.get_results_summary()
        
        # Radar Chart
        if results['stats']:
            st.subheader("Vulnerability Profile")
            df = pd.DataFrame(list(results['stats'].items()), columns=['Category', 'Vulnerability'])
            fig = px.line_polar(df, r='Vulnerability', theta='Category', line_close=True)
            fig.update_traces(fill='toself')
            st.plotly_chart(fig)

        if results['weakness']:
            st.error(f"⚠️ Your Primary Weakness: {results['weakness']}")
        
        st.divider()
        
        for score in engine.scores:
            # Only show analysis if the user was swayed significantly (e.g., > 10 points)
            if score['delta'] > 10:
                st.subheader(f"Round {score['round_id'] + 1}: {score['category']}")
                st.write(f"Technique: **{score['technique']}**")
                st.write(f"You were swayed by **{score['delta']} points**.")
                
                data = score['data']
                trigger = data['trigger_fragment']
                full_text = data['argument_text']
                
                # Split text to highlight trigger
                parts = re.split(f"({re.escape(trigger)})", full_text, flags=re.IGNORECASE)
                
                annotated_parts = []
                for part in parts:
                    if part.lower() == trigger.lower():
                        annotated_parts.append((part, score['technique'], "#faa"))
                    elif part:
                        annotated_parts.append(part)
                
                annotated_text(*annotated_parts)
                
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
