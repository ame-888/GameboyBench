import os
import base64
import cv2
from gameboy_controller import GameBoyController
import openai
import datetime
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not set in .env file")

# Define the system prompt for the LLM
system_prompt = """
You are an AI agent playing the game Pokémon Red on a GameBoy emulator. Your ultimate goal is to become the Pokémon Champion by defeating the Elite Four. To achieve this, you will need to explore the Kanto region, battle and capture Pokémon, challenge Gym Leaders to earn badges, and progress through the game's storyline.

Here are some basic tips to help you navigate the game:
- **Exploration**: Move around using the arrow keys (functions: press_up, press_down, press_left, press_right). Interact with NPCs, enter buildings, and explore new areas to advance the plot.
- **Battles**: When in battles, use the A button (press_a) to select moves or confirm actions, and the B button (press_b) to cancel or go back. You can also use the arrow keys to navigate menus.
- **Menus**: Press the Start button (press_start) to open the main menu, where you can manage your Pokémon, items, and save the game. Use the arrow keys and A button to navigate and select options.
- **Interactions**: Press the A button to talk to people, read signs, or interact with objects in the environment.
- **Progression**: Focus on collecting all 8 Gym badges, which will allow you to challenge the Elite Four. You’ll need to solve puzzles, defeat trainers, and make strategic decisions to succeed.

You will receive the current game screen as an image with each request. Based on the screen and your previous actions, decide which function(s) to call next. You can call multiple functions in a single response to press multiple buttons simultaneously (e.g., 'press_up' and 'press_a' to move up while pressing A). Separate multiple function calls with commas, like 'press_up, press_a'.

You will also see your last 100 interactions (frames, function calls and outcomes) to help you remember your recent actions and make better decisions.

Always respond with the function(s) you want to call, such as 'press_up' or 'press_a, press_right'. If you’re unsure, make your best guess based on typical Pokémon gameplay. Remember, your goal is to explore, battle, and progress toward becoming the Pokémon Champion.
"""


# **Tools Mapping**
# Maps function names (as strings) to their corresponding button strings.
tools_map = {
    "press_up": "up",
    "press_down": "down",
    "press_left": "left",
    "press_right": "right",
    "press_a": "a",
    "press_b": "b",
    "press_start": "start",
    "press_select": "select",
}

# **Tools Definition**
# Defines the functions available to the LLM in a format it can understand.
tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "press_up",
            "description": "Press the up button on the GameBoy",
            "parameters": {"type": "object", "properties": {}},  # No parameters needed
        },
    },
    {
        "type": "function",
        "function": {
            "name": "press_down",
            "description": "Press the down button on the GameBoy",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "press_left",
            "description": "Press the left button on the GameBoy",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "press_right",
            "description": "Press the right button on the GameBoy",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "press_a",
            "description": "Press the A button on the GameBoy",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "press_b",
            "description": "Press the B button on the GameBoy",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "press_start",
            "description": "Press the Start button on the GameBoy",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "press_select",
            "description": "Press the Select button on the GameBoy",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def encode_image(image):
    """Encode a NumPy image array to base64 string."""
    _, buffer = cv2.imencode(".png", image)
    return base64.b64encode(buffer).decode("utf-8")


def main():
    # Get ROM path from environment variable
    rom_path = os.getenv("ROM_PATH")
    if not rom_path:
        print("Error: ROM_PATH not set in .env file")
        return

    print("ROM path:", rom_path)

    # Initialize the GameBoy controller in headless mode
    gb = GameBoyController(
        rom_path,
        headless=True,  # No display needed for LLM agent
        sound_emulated=False,  # Disable sound for simplicity
        simulation_speed=0,  # Run at max speed (0 means unlimited)
    )

    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.x.ai/v1"
    )

    try:
        print("Starting game...")
        gb.start()
        gb.tick(60)  # Wait for game to load (1 second at 60 FPS)

        # Setup for screenshots with timestamped directory
        experiment_id = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshots_dir = f"screenshots_{experiment_id}"

        last_save_time = time.time()
        screenshot_counter = 0

        # Main loop parameters
        N = 30  # Make a decision every 30 frames
        frame_count = 0
        running = True
        current_buttons = []  # Buttons to press for the current decision period
        history = []  # History of past actions

        while running:
            if frame_count % N == 0:
                # Get the current screen
                screen = gb.get_screen_np()
                base64_image = encode_image(screen)

                # Construct user message with past actions and current frame
                user_content = [
                    {
                        "type": "text",
                        "text": "This is the most recent screen of the game. Which button should you press next?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                ]

                messages = [
                    {"role": "system", "content": system_prompt},
                ]

                if len(history) > 100:
                    messages.append(
                        {
                            "role": "user",
                            "content": "Note: History has been truncated to last 100 interactions...",
                        }
                    )

                messages.extend(history[-100:])
                messages.append(user_content)

                # Send request to LLM via OpenAI API
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Use a vision-capable model
                    messages=messages,
                    max_tokens=100,  # Allow for multiple function calls
                    tools=tools_definition,
                    tool_choice="required",
                    n=1,
                )

                history.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Which button should you press next?",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": "high",
                                },
                            },
                        ],
                    }
                )

                # Parse the LLM's response for multiple functions

                buttons_pressed = [
                    t.function.name
                    for t in response.choices[0].message.tool_calls
                    if t.function.name in tools_map
                ]

                if len(buttons_pressed) > 0:
                    current_buttons = buttons_pressed
                    history.append(
                        {
                            "role": "assistant",
                            "content": f"I press {' and'.join(buttons_pressed)}",
                        }
                    )
                else:
                    current_buttons = []
                    history.append(
                        {"role": "assistant", "content": "I press no button"}
                    )
            print("Buttons pressed:", current_buttons)
            # Execute the current action
            gb.press_and_tick([tools_map[b] for b in current_buttons])

            cv2.namedWindow("GameBoy", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("GameBoy", 480, 432)
            if frame_count % 2 == 0:
                screen = gb.get_screen_np()
                # Display the image with fixed window size matching GameBoy resolution (160x144)

                # Fix: Properly encode the image to base64
                _, buffer = cv2.imencode(".png", screen)
                base64_image = base64.b64encode(buffer).decode("utf-8")
                print(base64_image)

                cv2.imshow("GameBoy", screen)
                # Check for key press to exit
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    running = False

            # Save screenshot every 10 seconds
            current_time = time.time()
            if current_time - last_save_time > 10:
                screen = gb.get_screen_np()
                os.makedirs(screenshots_dir, exist_ok=True)
                cv2.imwrite(
                    os.path.join(
                        screenshots_dir, f"screenshot_{screenshot_counter:04d}.png"
                    ),
                    screen,
                )
                screenshot_counter += 1
                last_save_time = current_time

            frame_count += 1

            # Optional: Limit runtime for testing
            if frame_count > 10000:
                print("Reached frame limit, stopping.")
                print(history)
                running = False

    except Exception as e:
        print(f"Error: {e}")
    finally:
        gb.close()
        print("Game closed.")


if __name__ == "__main__":
    main()
