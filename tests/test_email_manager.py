
import unittest
from email_manager import EmailManagerApp
from list_messages import ListMessagesPage
from read_messages import ReadMessagesPage
from new_message import NewMessagePage
from label_messages import LabelMessagesPage


class TestEmailManagerApp(unittest.TestCase):

    def setUp(self):
        """Set up the EmailManagerApp instance for testing."""
        self.app = EmailManagerApp()
        self.app.update()  # Ensure that the app window is created

    def test_list_messages_button(self):
        """Test that clicking the 'List Messages' button switches to ListMessagesPage."""
        self.app.indicate(self.app.list_message_indicator, ListMessagesPage)

        # Wait for the UI to process the update
        self.app.update_idletasks()

        # Check if the active page is ListMessagesPage
        current_page = type(self.app.main_frame.winfo_children()[0])
        self.assertEqual(current_page, ListMessagesPage, f"Expected ListMessagesPage but got {current_page}")

    def test_read_message_button(self):
        """Test that clicking the 'Read Message' button switches to ReadMessagesPage."""
        # First, set a valid message ID
        self.app.id_txt.insert(0, "1")  # Example valid ID

        self.app.indicate(self.app.read_message_indicator, ReadMessagesPage)

        # Wait for the UI to process the update
        self.app.update_idletasks()

        # Check if the active page is ReadMessagesPage
        current_page = type(self.app.main_frame.winfo_children()[0])
        self.assertEqual(current_page, ReadMessagesPage, f"Expected ReadMessagesPage but got {current_page}")


    def test_invalid_message_id(self):
        """Tests error handling when an invalid ID is entered."""
        self.app.id_txt.insert(0, "abc")  # Inserting invalid ID
        self.app.show_frame(ReadMessagesPage)  # Attempt to switch page
        assert self.app.id_txt.get() == ""  # Should be cleared after error

    def test_new_message_button(self):
        """Test that clicking the 'New Message' button switches to NewMessagesPage."""
        self.app.indicate(self.app.new_message_indicator, NewMessagePage)

        # Wait for the UI to process the update
        self.app.update_idletasks()

        # Check if the active page is NewMessagesPage
        current_page = type(self.app.main_frame.winfo_children()[0])
        self.assertEqual(current_page, NewMessagePage, f"Expected NewMessagesPage but got {current_page}")

    def test_label_messages_button(self):
        """Test that clicking the 'Label Messages' button switches to LabelMessagesPage."""
        self.app.indicate(self.app.label_message_indicator, LabelMessagesPage)

        # Wait for the UI to process the update
        self.app.update_idletasks()

        # Check if the active page is LabelMessagesPage
        current_page = type(self.app.main_frame.winfo_children()[0])
        self.assertEqual(current_page, LabelMessagesPage, f"Expected LabelMessagesPage but got {current_page}")

    def test_sidebar_indicators(self):
        """Test that sidebar indicators are updated correctly when switching pages."""
        # Switch to ListMessagesPage and check if indicator is updated
        self.app.indicate(self.app.list_message_indicator, ListMessagesPage)
        self.assertEqual(self.app.list_message_indicator.cget("bg"), '#1155cc')

        # Switch to ReadMessagesPage and check if indicator is updated
        self.app.indicate(self.app.read_message_indicator, ReadMessagesPage)
        self.assertEqual(self.app.read_message_indicator.cget("bg"), '#1155cc')

        # Switch to NewMessagesPage and check if indicator is updated
        self.app.indicate(self.app.new_message_indicator, NewMessagePage)
        self.assertEqual(self.app.new_message_indicator.cget("bg"), '#1155cc')

        # Switch to LabelMessagesPage and check if indicator is updated
        self.app.indicate(self.app.label_message_indicator, LabelMessagesPage)
        self.assertEqual(self.app.label_message_indicator.cget("bg"), '#1155cc')


if __name__ == '__main__':
    unittest.main()



