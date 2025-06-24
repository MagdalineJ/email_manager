import unittest
from unittest.mock import MagicMock,patch
import tkinter as tk
import message_manager as messages
from list_messages import ListMessagesPage

class TestListMessagesPage(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Setting up a Tkinter window and ListMessagesPage
        self.root = tk.Tk()
        self.controller = MagicMock()  # Mock controller
        self.page = ListMessagesPage(self.root, self.controller)
        self.page.pack()

        # Mocking the messages module to simulate message data
        messages.messages = {
            1: MagicMock(sender="alice@example.com", recipient="bob@example.com", subject="Meeting", info=MagicMock(return_value="**")),
            2: MagicMock(sender="bob@example.com", recipient="alice@example.com", subject="Project Update", info=MagicMock(return_value="***")),
        }

    def tearDown(self):
        """Clean up the environment after each test."""
        self.root.destroy()

    def test_toggle_search_button_enable(self):
        """Test if the search button is enabled when there is input in the filter entry."""
        self.page.filter_entry.insert(0, "Alice")
        self.page.toggle_search_button()  # Simulate key release event
        self.assertEqual(self.page.search_button["state"], "normal")

    def test_toggle_search_button_disable(self):
        """Test if the search button is disabled when there is no input in the filter entry."""
        self.page.filter_entry.delete(0, tk.END)
        self.page.toggle_search_button()  # Simulate key release event
        self.assertEqual(self.page.search_button["state"], "disabled")

    @patch("tkinter.messagebox.showwarning")
    def test_filter_messages_no_matches(self,mock_showwarning):
        """Test the filter function when no messages match the filter criteria."""
        #filter text that won't match any message
        self.page.filter_entry.insert(0, "nonexistent@example.com")
        self.page.filter_messages()

        # Checking if showwarning was called with the expected message
        mock_showwarning.assert_called_once_with('No Matches', "No messages found for 'nonexistent@example.com' under 'Sender'.")



    def test_refresh(self):
        """Test the refresh button's behavior."""
        # Simulate clicking the refresh button
        self.page.refresh_button.invoke()

        # Checking if the frame is refreshed (if it's calling show_frame correctly)
        self.controller.show_frame.assert_called_with(ListMessagesPage)

    def test_list_messages(self):
        """Test the list_messages method to see if it populates the text area with all messages."""
        # Calling the list_messages method
        self.page.list_messages()

        # Checking if the text area has been populated with message data
        content = self.page.list_txt.get("1.0", tk.END).strip()
        self.assertIn("**", content)
        self.assertIn("***", content)
        self.assertIn("1", content)
        self.assertIn("2", content)

if __name__ == "__main__":
    unittest.main()
