import unittest
from message import Message  # Assuming Message class is in 'message.py'

class TestMessage(unittest.TestCase):

    def setUp(self):
        """Setup method for creating Message instances to be used in tests."""
        self.message = Message(sender="john@example.com", recipient="jane@example.com",
                               subject="Test Subject", message="This is a test message",
                               label="Important", priority=3)
        self.message_no_priority = Message(sender="alice@example.com", recipient="bob@example.com",
                                            subject="Another Subject", message="No priority message",
                                            label="Unread",priority=0)

    def test_message_initialization(self):
        """Test if the message is correctly initialized."""
        self.assertEqual(self.message.sender, "john@example.com")
        self.assertEqual(self.message.recipient, "jane@example.com")
        self.assertEqual(self.message.subject, "Test Subject")
        self.assertEqual(self.message.content, "This is a test message")
        self.assertEqual(self.message.label, "Important")
        self.assertEqual(self.message.priority, 3)

        # Test default priority value
        self.assertEqual(self.message_no_priority.priority, 0)

    def test_info_method_with_priority(self):
        """Test if the info method returns the correct message formatting, including priority stars."""
        expected_info = ' ***      john@example.com            Important   Test Subject \n'
        self.assertEqual(self.message.info(), expected_info)

    def test_info_method_without_priority(self):
        """Test if the info method works correctly when there is no priority."""
        expected_info = '          alice@example.com           Unread      Another Subject \n'
        self.assertEqual(self.message_no_priority.info(), expected_info)

    def test_stars_method(self):
        """Test if the stars method correctly returns a string with stars based on priority."""
        self.assertEqual(self.message.stars(), "***")  # Three stars for priority 3
        self.assertEqual(self.message_no_priority.stars(), "")  # No stars for default priority 0

    def test_star_with_zero_priority(self):
        """Test if zero priority returns no stars."""
        self.assertEqual(self.message_no_priority.stars(), "")

if __name__ == "__main__":
    unittest.main()
