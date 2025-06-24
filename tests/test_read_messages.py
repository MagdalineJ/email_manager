import unittest
from unittest.mock import MagicMock
import tkinter as tk
from read_messages import ReadMessagesPage  # Import the actual class
import message_manager as messages
from list_messages import ListMessagesPage  # Assuming this is the correct import


class TestReadMessagesPage(unittest.TestCase):

    def setUp(self):
        """Set up the test environment by creating a root Tkinter window and controller mock."""
        self.root = tk.Tk()  # Create a root window for Tkinter
        self.controller = MagicMock()  # Mock the controller (to handle frame changes)
        self.message_id = 1  # Assume we have a message with ID = 1

        # Mock the messages module methods
        messages.get_message_by_id = MagicMock()
        messages.set_priority = MagicMock()
        messages.delete_message = MagicMock()

    def test_read_message_found(self):
        """Test the scenario where the message is found and displayed."""
        # Mock message object with attributes (instead of returning a dict)
        mock_message = MagicMock()
        mock_message.sender = 'john@example.com'
        mock_message.recipient = 'jane@example.com'
        mock_message.subject = 'Test Message'
        mock_message.content = 'This is a test message content.'

        messages.get_message_by_id.return_value = mock_message

        # Create the ReadMessagesPage and verify widgets
        read_page = ReadMessagesPage(self.root, self.controller, self.message_id)
        read_page.pack()

        # Check if the message data is populated correctly in the entry widgets
        self.assertEqual(read_page.sender_txt.get(), 'john@example.com')
        self.assertEqual(read_page.recipient_txt.get(), 'jane@example.com')
        self.assertEqual(read_page.subject_txt.get(), 'Test Message')
        self.assertEqual(read_page.content_txt.get("1.0", tk.END).strip(), 'This is a test message content.')

        # Check if the priority text field is initialized
        self.assertEqual(read_page.priority_txt.get(), "")

    def test_read_message_not_found(self):
        """Test the scenario where the message is not found."""
        # Mock get_message_by_id to return None (message not found)
        messages.get_message_by_id.return_value = None

        # Create the ReadMessagesPage
        read_page = ReadMessagesPage(self.root, self.controller, self.message_id)
        read_page.pack()

        # Check that we navigate to the ListMessagesPage after message not found
        self.controller.show_frame.assert_called_once()  # Ensure that the frame switch happened
        # Check if the frame name is ListMessagesPage
        self.assertEqual(self.controller.show_frame.call_args[0][0], ListMessagesPage)

    def test_update_priority_valid(self):
        """Test the scenario when the priority is updated correctly."""
        # Mock message object with attributes
        mock_message = MagicMock()
        mock_message.sender = 'john@example.com'
        mock_message.recipient = 'jane@example.com'
        mock_message.subject = 'Test Message'
        mock_message.content = 'This is a test message content.'

        messages.get_message_by_id.return_value = mock_message

        # Create the ReadMessagesPage
        read_page = ReadMessagesPage(self.root, self.controller, self.message_id)
        read_page.pack()

        # Simulate entering a valid priority value
        read_page.priority_txt.insert(tk.END, '3')  # Insert a valid priority

        # Mock the set_priority method
        messages.set_priority.return_value = None

        # Call the update_priority method
        read_page.update_priority()

        # Ensure set_priority was called with correct parameters
        messages.set_priority.assert_called_once_with(self.message_id, 3)

    def test_update_priority_invalid(self):
        """Test the scenario when an invalid priority value is entered."""
        # Mock message object with attributes
        mock_message = MagicMock()
        mock_message.sender = 'john@example.com'
        mock_message.recipient = 'jane@example.com'
        mock_message.subject = 'Test Message'
        mock_message.content = 'This is a test message content.'

        messages.get_message_by_id.return_value = mock_message

        # Create the ReadMessagesPage
        read_page = ReadMessagesPage(self.root, self.controller, self.message_id)
        read_page.pack()

        # Simulate entering an invalid priority value
        read_page.priority_txt.insert(tk.END, '10')  # Invalid priority value (greater than 5)

        # Mock the set_priority method
        messages.set_priority.return_value = None

        # Call the update_priority method
        read_page.update_priority()

        # Ensure that set_priority was not called
        messages.set_priority.assert_not_called()

    def test_delete_message(self):
        """Test the scenario when a message is deleted."""
        # Mock message object with attributes
        mock_message = MagicMock()
        mock_message.sender = 'john@example.com'
        mock_message.recipient = 'jane@example.com'
        mock_message.subject = 'Test Message'
        mock_message.content = 'This is a test message content.'

        messages.get_message_by_id.return_value = mock_message

        # Create the ReadMessagesPage
        read_page = ReadMessagesPage(self.root, self.controller, self.message_id)
        read_page.pack()

        # Simulate clicking the delete button
        read_page.delete_message()

        # Ensure delete_message was called
        messages.delete_message.assert_called_once_with(self.message_id)

        # Ensure that the controller navigates to ListMessagesPage after deletion
        self.controller.show_frame.assert_called_once_with(ListMessagesPage)


if __name__ == '__main__':
    unittest.main()
