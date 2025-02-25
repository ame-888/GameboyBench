# 🎮 Gambeboy eval

![screenshot_0001](https://github.com/user-attachments/assets/538ca2fb-38ab-4dad-84dc-eb236be90c0b)

This project uses an AI agent powered by a Large Language Model (LLM) to play GameBoy games on an emulator. While designed to work with various GameBoy titles, we initially focus on Pokémon Red as our test case. The agent receives the game screen as input, analyzes the current state, and decides which buttons to press to progress through the game. The agent can take notes and decide to wait as well

## Features

- Fully autonomous gameplay using LLM-based decision making
- Visual processing of GameBoy screen captures
- Configurable decision frequency and emulation speed
- Automatic screenshot capture for monitoring progress
- History tracking to provide context for decision making

## Requirements

- Python 3.8+
- OpenAI API key or compatible LLM API
- GameBoy ROM file (not included)

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   uv sync
   ```
3. Create a `.env` file with the following variables:
   ```
   OPENAI_API_KEY=your_api_key_here
   ROM_PATH=path/to/your/pokemon_red.gb
   ```

## Usage

Run the main script to start the AI agent:


```bash
python llm.py
```


The program will:
- Initialize the GameBoy emulator with the specified ROM
- Start the game and begin capturing screen frames
- Send these frames to the LLM for analysis
- Execute the button presses recommended by the LLM
- Save screenshots periodically to track progress
- Display the current game screen in a window

You can press 'q' in the display window to exit the program.

## Configuration

You can modify the following parameters in `llm.py`:
- `N`: How frequently the LLM makes decisions (in frames)
- `emulation_speed`: Controls how fast the game runs
- Screenshot frequency (default: every 10 seconds)
- Maximum runtime (default: 10,000 frames)

## How It Works

1. The GameBoy emulator runs the Pokémon ROM in headless mode
2. Every N frames, the current screen is captured and encoded
3. The screen image and recent history are sent to the LLM
4. The LLM analyzes the game state and decides which buttons to press
5. The emulator executes these button presses
6. The process repeats, with the agent learning from its history

## Project Structure

- `llm.py`: Main script that handles the LLM integration and game loop
- `gameboy_controller.py`: Interface to the GameBoy emulator
- `.env`: Configuration file for API keys and ROM path

## Limitations

- The agent's performance depends on the quality of the LLM and its understanding of Pokémon gameplay
- Decision-making is limited by the context window of the LLM
- The agent has no memory beyond its recent history

## License

MIT

## Acknowledgments

- PyBoy for the GameBoy emulation
