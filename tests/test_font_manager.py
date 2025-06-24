import unittest
import tkinter as tk
import tkinter.font as tkfont
from font_manager import configure  # Replace 'your_module' with the actual module name


class TestFontConfiguration(unittest.TestCase):
    def setUp(self):
        """Set up a Tkinter root window to test font configuration."""
        self.root = tk.Tk()  # Create a root window
        self.root.withdraw()  # Hide the root window, since we only care about font configuration

    def test_default_font(self):
        """Test if the default font is set to 'Segoe UI' and size 11."""
        configure()  # Call the configure function

        # Get the configured default font
        default_font = tkfont.nametofont("TkDefaultFont")

        self.assertEqual(default_font.cget("family"), "Segoe UI")
        self.assertEqual(default_font.cget("size"), 11)


    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()  # Destroy the Tkinter root window


if __name__ == "__main__":
    unittest.main()
