# 🎮 Gambeboy eval

<img width="1046" alt="Screenshot 2025-02-25 at 09 27 53" src="https://github.com/user-attachments/assets/d8894780-78a6-426a-9ffc-a139e10d5c69" />

This project uses an AI agent powered by a Large Language Model (LLM) to play GameBoy games on an emulator. While designed to work with various GameBoy titles, we initially focus on Pokémon Red as our test case. The agent receives the game screen as input, analyzes the current state, and decides which buttons to press to progress through the game. The agent can take notes and decide to wait as well


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
- Execute the button presses recommended by the LLM and take notes
- Save screenshots periodically to track progress
- Display the current game screen in a window

You can press 'q' in the display window to exit the program.

## Configuration

```python

@dataclass
class GameConfig:
    rom_path: str
    max_steps: int
    emulation_speed: float

```

You can modify the following parameters in `llm.py`:
- `max_steps`: How many steps the llm should take
- `emulation_speed`: Controls how fast the game runs
- Screenshot frequency (default: every 10 seconds)
- Maximum runtime (default: 10,000 frames)
- Eval function (currently only implemented for PokemonRed)

## Project Structure

- `agent_play.py`: Main script that handles the LLM integration and game loop
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
