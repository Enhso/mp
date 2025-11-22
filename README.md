# MindPatch Prototype

MindPatch is an interactive Streamlit application designed to help users identify their cognitive vulnerabilities and resistance to persuasion techniques.

## Overview

The application presents users with a series of claims and arguments. In each round, the user:
1.  **Takes a Stance:** Sets their initial agreement level with a claim (0-100).
2.  **Locks In:** Commits to this initial position.
3.  **Faces an Argument:** Reads a counter-argument or additional context designed to challenge their view.
4.  **Re-evaluates:** Adjusts their stance based on the new information.

At the end of the session, the "X-Ray Analysis" reveals:
-   **Primary Weakness:** The specific rhetorical technique that swayed the user the most.
-   **Detailed Breakdown:** A round-by-round analysis of where the user changed their mind significantly, highlighting the specific "trigger fragments" in the text and providing "antidotes" (defense strategies) against those techniques.

## Features

-   **Interactive Game Loop:** Engaging flow of claim evaluation and re-evaluation.
-   **Real-time Scoring:** Tracks how much a user's opinion shifts ("delta") in response to different arguments.
-   **Visual Text Analysis:** Uses `st-annotated-text` to highlight specific rhetorical triggers within the arguments.
-   **Educational Feedback:** Provides "antidotes" to help users recognize and resist manipulative techniques in the future.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Enhso/mp.git
    cd mp
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser (usually at `http://localhost:8501`).

## Project Structure

-   `app.py`: The main Streamlit application entry point and UI logic.
-   `game_engine.py`: Core game logic, including state management, scoring, and data loading.
-   `data/game_data.json`: JSON file containing the game content (claims, arguments, triggers, antidotes).
-   `tests/`: Unit tests for the game engine.

## Development

To run the tests:

```bash
pytest
```
