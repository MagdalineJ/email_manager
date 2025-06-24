import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from label_messages import LabelMessagesPage  # Import the class you're testing
import message_manager as messages  # Assuming this is where your message manager functions reside



class TestLabelMessagesPage(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.root = tk.Tk()  # Create a root window for Tkinter
        self.controller = MagicMock()  # Mock the controller (for frame navigation)

        # Create an instance of the LabelMessagesPage
        self.page = LabelMessagesPage(self.root, self.controller)
        self.page.pack()

        # Mock messagebox methods
        self.showerror_patch = patch('tkinter.messagebox.showerror').start()
        self.showinfo_patch = patch('tkinter.messagebox.showinfo').start()

        # Add cleanup after tests
        self.addCleanup(patch.stopall)

    def tearDown(self):
        """Clean up after each test."""
        pass

    @patch('message_manager.list_all')
    def test_list_labelled_messages(self, mock_list_all):
        """Test if the label filter works and lists the correct messages."""
        label = "Work"
        mock_list_all.return_value = "1 3 sender@example.com Work Subject 1\n2 4 recipient@example.com Work Subject 2\n"

        # Simulate selecting the "Work" label and clicking the button to list messages
        self.page.label_var.set(label)  # Set the label to "Work"
        self.page.list_labelled_messages()

        # Check that list_all was called with the correct label
        mock_list_all.assert_called_with(label)

        # Check that the messagebox showerror is not called (as there are messages)
        self.showerror_patch.assert_not_called()

        # Check that the list_txt widget contains the formatted messages
        self.assertIn("Subject 1", self.page.list_txt.get("1.0", tk.END))
        self.assertIn("Subject 2", self.page.list_txt.get("1.0", tk.END))

    @patch('message_manager.list_all')
    def test_list_labelled_messages_no_results(self, mock_list_all):
        """Test if no results found for a label."""
        label = "Work"
        mock_list_all.return_value = ""  # No messages found for the label

        # Simulate selecting the "Work" label and clicking the button to list messages
        self.page.label_var.set(label)
        self.page.list_labelled_messages()

        # Check that list_all was called with the correct label
        mock_list_all.assert_called_with(label)

        # Check that error messagebox was called (no messages found)
        self.showerror_patch.assert_called_with("Empty List", "No Messages Found!")

        # Check that the text widget has the correct message
        self.assertIn("No messages found with the Work label.", self.page.list_txt.get("1.0", tk.END))

    @patch('message_manager.set_label')
    def test_add_label_to_message(self, mock_set_label):
        """Test if adding a label to a message works correctly."""
        label = "Important"
        message_id = "1"

        # Simulate entering a message ID and selecting a label
        self.page.label_var.set(label)
        self.page.msg_id_txt.insert(0, message_id)

        # Mock the existence of a message
        messages.messages = {1: MagicMock()}  # Mock the messages dictionary with a message ID 1

        # Simulate clicking the "Add Label" button
        self.page.add_label_to_message()

        # Check that set_label was called with the correct message ID and label
        mock_set_label.assert_called_with(int(message_id), label)

        # Check that success messagebox is called
        self.showinfo_patch.assert_called_with("Success", f"Label '{label}' added to message {message_id}.")

    @patch('message_manager.set_label')
    def test_add_label_to_non_existent_message(self, mock_set_label):
        """Test if adding a label to a non-existent message shows an error."""
        label = "Important"
        message_id = "999"  # Non-existent message ID

        # Simulate entering a message ID and selecting a label
        self.page.label_var.set(label)
        self.page.msg_id_txt.insert(0, message_id)

        # Mock the absence of the message ID
        messages.messages = {1: MagicMock()}  # Only message ID 1 exists

        # Simulate clicking the "Add Label" button
        self.page.add_label_to_message()

        # Check that set_label was NOT called since message ID does not exist
        mock_set_label.assert_not_called()

        # Check that error messagebox is called
        self.showerror_patch.assert_called_with("Error", "Message ID not found.")

    def test_list_labelled_messages_no_label_selected(self):
        """Test if error is shown when no label is selected."""
        # Simulate not selecting any label
        self.page.label_var.set("")  # Empty label selection

        # Simulate clicking the "List Messages" button
        self.page.list_labelled_messages()

        # Check that the error messagebox is called
        self.showerror_patch.assert_called_with("Error", "Please select a label.")

    def test_add_label_to_message_no_label_selected(self):
        """Test if error is shown when no label is selected while adding label to a message."""
        # Simulate not selecting any label
        self.page.label_var.set("")  # Empty label selection

        # Simulate clicking the "Add Label" button
        self.page.add_label_to_message()

        # Check that the error messagebox is called
        self.showerror_patch.assert_called_with("Error", "Please select a label.")

    def test_add_label_to_message_invalid_id(self):
        """Test if error is shown when invalid message ID is provided."""
        # Simulate entering an invalid message ID
        self.page.msg_id_txt.insert(0, "invalid_id")

        # Simulate clicking the "Add Label" button
        self.page.add_label_to_message()

        # Check that the error messagebox is called
        self.showerror_patch.assert_called_with("Error", "Please select a label.")


if __name__ == "__main__":
    unittest.main()
