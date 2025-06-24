
import unittest
from unittest.mock import MagicMock
import tkinter as tk
from new_message import NewMessagePage
from list_messages import ListMessagesPage


class TestNewMessagesPage(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.root = tk.Tk()  # Create a root window for Tkinter
        self.controller = MagicMock()  # Mock the controller (for frame navigation)

        # Create an instance of the NewMessagesPage
        self.page = NewMessagePage(self.root, self.controller)
        self.page.pack()

        # Mock the messagebox functions
        self.showerror_patch = self.patch('tkinter.messagebox.showerror')
        self.showinfo_patch = self.patch('tkinter.messagebox.showinfo')

        # Patch the new_message function from message_manager
        self.new_message_patch = self.patch('message_manager.new_message')

    def patch(self, name):
        """Helper to patch tkinter's messagebox methods."""
        patcher = unittest.mock.patch(name)
        mock = patcher.start()
        self.addCleanup(patcher.stop)
        return mock


    def test_send_with_missing_fields(self):
        """Test if missing fields show error."""
        # Simulate clicking the send button
        self.page.sender_txt.insert(0, "")  # Empty sender field
        self.page.recipient_txt.insert(0, "recipient@example.com")
        self.page.subject_txt.insert(0, "Test subject")
        self.page.content_txt.insert("1.0", "Test message content.")
        self.page.priority_txt.insert(0, "3")

        # Call send method
        self.page.send()

        # Check that error messagebox is called
        self.showerror_patch.assert_called_with("Error", "All fields must be filled!")

    def test_send_with_invalid_email(self):
        """Test if invalid email formats show error."""
        self.page.sender_txt.insert(0, "invalid-email")  # Invalid sender email
        self.page.recipient_txt.insert(0, "recipient@example.com")
        self.page.subject_txt.insert(0, "Test subject")
        self.page.content_txt.insert("1.0", "Test message content.")
        self.page.priority_txt.insert(0, "3")

        # Call send method
        self.page.send()

        # Check that error messagebox is called for invalid email
        self.showerror_patch.assert_called_with("Error", "Invalid email format!")

    def test_send_with_invalid_priority(self):
        """Test if invalid priority (not between 0 and 5) shows error."""
        self.page.sender_txt.insert(0, "sender@example.com")
        self.page.recipient_txt.insert(0, "recipient@example.com")
        self.page.subject_txt.insert(0, "Test subject")
        self.page.content_txt.insert("1.0", "Test message content.")
        self.page.priority_txt.insert(0, "10")  # Invalid priority (outside range)

        # Call send method
        self.page.send()

        # Check that error messagebox is called for invalid priority
        self.showerror_patch.assert_called_with("Error", "Priority must be between 0 and 5!")

    def test_send_with_valid_input(self):
        """Test if a valid message is sent correctly."""

        self.page.sender_txt.insert(0, "sender@example.com")
        self.page.recipient_txt.insert(0, "recipient@example.com")
        self.page.subject_txt.insert(0, "Test subject")
        self.page.content_txt.insert("1.0", "Test message content.")
        self.page.priority_txt.insert(0, "3")  # Valid priority

        self.page.send()  # Call the send method

        # Check if new_message is called with correct arguments
        self.new_message_patch.assert_called_once_with(
            "sender@example.com",
            "recipient@example.com",
            "Test subject",
            "Test message content.",
            "unread",  # Make sure this matches exactly with what send() uses
            3
        )

        # Check that success messagebox is called
        self.showinfo_patch.assert_called_once_with("Status", "Message was sent successfully!")

    def test_cancel_button(self):
        """Test if the cancel button navigates to the list of messages."""
        # Simulate clicking the cancel button
        self.page.close()

        # Check that controller's show_frame method is called to switch to ListMessagesPage
        self.controller.show_frame.assert_called_with(ListMessagesPage)


if __name__ == '__main__':
    unittest.main()
