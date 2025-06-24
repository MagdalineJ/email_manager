import unittest
from unittest.mock import patch
import message_manager  # Replace with the actual import path of your message_manager


class Message:
    def __init__(self, sender, recipient, subject, content, label, priority):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.content = content
        self.label = label
        self.priority = priority


class TestMessageManager(unittest.TestCase):


    @patch("message_manager.open", new_callable=unittest.mock.mock_open)
    @patch("message_manager.os.path.exists", return_value=False)  # Simulate file does not exist
    @patch("message_manager.csv.writer")
    def test_initialize_csv(self, mock_writer, mock_exists, mock_open):
        """Test that CSV file is initialized if it doesn't exist."""
        message_manager.initialize_csv()

        # Ensure the CSV writer writes the header at least once
        mock_writer.return_value.writerow.assert_any_call(message_manager.HEADERS)

    @patch("message_manager.load_messages")
    def test_load_messages(self, mock_load_messages):
        """Test loading messages from CSV."""
        mock_load_messages.return_value = {
            1: Message('test1@example.com', 'test2@example.com', 'Test Subject 1', 'Test Content 1', 'Unread', 1),
            2: Message('test3@example.com', 'test4@example.com', 'Test Subject 2', 'Test Content 2', 'Read', 2)
        }
        messages = message_manager.load_messages()
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[1].sender, 'test1@example.com')

    def test_new_message(self):
        """Test creating a new message."""
        test_sender = 'sender@example.com'
        test_recipient = 'recipient@example.com'
        test_subject = 'Test Subject'
        test_content = 'Test Content'
        test_label = 'Unread'
        test_priority = 1

        # Capture initial message count
        initial_count = len(message_manager.messages)

        # Add new message
        message_manager.new_message(test_sender, test_recipient, test_subject, test_content, test_label, test_priority)

        # Ensure the message count increased by 1
        self.assertEqual(len(message_manager.messages), initial_count + 1)

        # Get the last added message to validate its contents
        last_id = max(message_manager.messages.keys())
        new_msg = message_manager.messages[last_id]

        self.assertEqual(new_msg.sender, test_sender)
        self.assertEqual(new_msg.recipient, test_recipient)
        self.assertEqual(new_msg.subject, test_subject)
        self.assertEqual(new_msg.content, test_content)
        self.assertEqual(new_msg.label, test_label)
        self.assertEqual(new_msg.priority, test_priority)

    @patch("message_manager.save_all_messages")
    def test_save_all_messages(self, mock_save_all_messages):
        """Test saving messages to CSV."""
        test_messages = {
            1: Message('test1@example.com', 'test2@example.com', 'Test Subject 1', 'Test Content 1', 'Unread', 1),
            2: Message('test3@example.com', 'test4@example.com', 'Test Subject 2', 'Test Content 2', 'Read', 2)
        }
        message_manager.save_all_messages(test_messages)

        # Check that the save_all_messages method was called
        mock_save_all_messages.assert_called_once_with(test_messages)

    def test_delete_message(self):
        """Test deleting a message."""
        test_messages = {
            1: Message('test1@example.com', 'test2@example.com', 'Test Subject 1', 'Test Content 1', 'Unread', 1)
        }

        # Simulate deleting the message
        del test_messages[1]

        # Check that the message was deleted
        self.assertNotIn(1, test_messages)

    def test_get_message_by_id(self):
        """Test retrieving a message by ID."""
        test_messages = {
            1: Message('test1@example.com', 'test2@example.com', 'Test Subject 1', 'Test Content 1', 'Unread', 1)
        }

        # Simulate retrieving a message by ID
        message = test_messages.get(1)

        self.assertIsNotNone(message)
        self.assertEqual(message.subject, 'Test Subject 1')

    def test_list_all(self):
        """Test the listing of all messages."""
        test_messages = {
            1: Message('test1@example.com', 'test2@example.com', 'Test Subject 1', 'Test Content 1', 'Unread', 1),
            2: Message('test3@example.com', 'test4@example.com', 'Test Subject 2', 'Test Content 2', 'Read', 2)
        }

        # Check the length of all messages
        self.assertEqual(len(test_messages), 2)

    def test_set_label(self):
        """Test setting the label of a message."""
        test_messages = {
            1: Message('test1@example.com', 'test2@example.com', 'Test Subject 1', 'Test Content 1', 'Unread', 1)
        }

        # Change the label of the message
        test_messages[1].label = 'Read'

        # Check the updated label
        self.assertEqual(test_messages[1].label, 'Read')

    def test_set_priority(self):
        """Test setting the priority of a message."""
        test_messages = {
            1: Message('test1@example.com', 'test2@example.com', 'Test Subject 1', 'Test Content 1', 'Unread', 1)
        }

        # Change the priority of the message
        test_messages[1].priority = 5

        # Check the updated priority
        self.assertEqual(test_messages[1].priority, 5)


if __name__ == "__main__":
    unittest.main()