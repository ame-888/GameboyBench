from gameboy_controller import GameBoyController
import dotenv
import os
import random
import cv2

dotenv.load_dotenv()

# Button mappings for terminal input
BUTTON_MAPPINGS = {
    "w": "up",
    "s": "down",
    "a": "left",
    "d": "right",
    "j": "a",
    "k": "b",
    "p": "start",
    "o": "select",
}


def main():

    rom_path = os.getenv("ROM_PATH")
    if not rom_path:
        print("Error: ROM_PATH not set in .env file")
        return

    print("ROM path:", rom_path)

    # Create the GameBoy controller
    gb = GameBoyController(
        rom_path, headless=True, sound_emulated=True, simulation_speed=10
    )

    try:
        print("Starting game...")
        gb.start()
        gb.tick(60)  # Wait for game to load

        print("\nGame is running! Use the following controls:")
        print(" - W/A/S/D: Move Up/Left/Down/Right")
        print(" - J: A button")
        print(" - K: B button")
        print(" - P: Start")
        print(" - O: Select")
        print(" - Space: Release all buttons")
        print(" - Q: Quit")
        # Main game loop
        frame_count = 0
        running = True
        while running:
            # Process pressed keys
            # Randomly select buttons to press
            buttons = []
            if random.random() < 0.5:  # 30% chance to press buttons
                possible_buttons = [
                    "up",
                    "down",
                    "left",
                    "right",
                    "a",
                    "b",
                    "start",
                    "select",
                ]
                num_buttons = random.randint(1, 3)  # Press 1-3 buttons at a time
                buttons = random.sample(possible_buttons, num_buttons)
            gb.press_and_tick(buttons)

            # Render screen every 3 frames
            frame_count += 1
            cv2.namedWindow("GameBoy", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("GameBoy", 480, 432)
            if frame_count % 2 == 0:
                screen = gb.get_screen_np()
                # Display the image with fixed window size matching GameBoy resolution (160x144)

                base64_image = cv2.imencode(".png", screen)[1].tobytes()
                base64_image = base64_image.decode("utf-8")
                print(base64_image)

                cv2.imshow("GameBoy", screen)
                # Check for key press to exit
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    running = False

    except Exception as e:
        print(f"Error: {e}")
    finally:
        gb.close()
        cv2.destroyAllWindows()
        print("Game closed.")


if __name__ == "__main__":
    main()
