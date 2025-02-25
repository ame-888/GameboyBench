from typing import List
from pyboy import PyBoy


class GameBoyController:
    """A wrapper class for controlling a GameBoy emulator through Python."""

    def __init__(
        self,
        rom_path,
        headless=False,
        sound_emulated=False,
        emulation_speed=1,
    ):
        """Initialize the GameBoy emulator with the specified ROM."""
        self.pyboy = PyBoy(
            rom_path,
            window="null" if headless else "SDL2",
            sound_emulated=sound_emulated,
        )
        self.pyboy.set_emulation_speed(emulation_speed)

    def start(self):
        """Start the emulator."""
        self.pyboy.tick()

    def tick(self, n=1):
        """Run the emulator for n frames."""
        for _ in range(n):
            self.pyboy.tick()

    def press_and_tick(self, buttons: List[str], frames=5):
        for button in buttons:
            self.pyboy.button_press(button)

        self.tick(frames)

        for button in buttons:
            self.pyboy.button_release(button)

    def get_screen_np(self):
        return self.pyboy.screen.ndarray

    def get_screen(self):
        return self.pyboy.screen.image

    def get_memory_value(self, address):
        return self.pyboy.get_memory_value(address)

    def close(self):
        self.pyboy.stop()
