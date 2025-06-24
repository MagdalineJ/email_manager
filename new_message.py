import tkinter as tk
import tkinter.scrolledtext as tkst  # For displaying messages
import re
from tkinter import messagebox # Import ttk for dropdown

from list_messages import ListMessagesPage
from message_manager import  new_message


class NewMessagePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Store the controller reference
        # Set background color for the frame
        self.config(bg="#1E2136")
        # Update status label
        if hasattr(self.master.master, "status_lbl"):
            self.master.master.status_lbl.config(text="New Message \n\nbutton was clicked!")

        tk.Label(self, bg="#1E2136",text='Compose a New Message', font=('Bold', 20)).pack(pady=5)

        form_frame = tk.Frame(self)
        form_frame.configure(bg="#1E2136")
        form_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Sender
        sender_frame = tk.Frame(form_frame)
        sender_frame.pack(fill="x", pady=2)
        sender_frame.configure(bg="#1E2136")
        tk.Label(sender_frame,bg="#1E2136", text="From:    ").pack(side="left", padx=5)
        self.sender_txt = tk.Entry(sender_frame, width=30)
        self.sender_txt.pack(side="left", fill="x", expand=True, padx=5)

        # Recipient
        recipient_frame = tk.Frame(form_frame)
        recipient_frame.pack(fill="x", pady=2)
        recipient_frame.configure(bg="#1E2136")
        tk.Label(recipient_frame, bg="#1E2136",text="To:        ").pack(side="left", padx=5)
        self.recipient_txt = tk.Entry(recipient_frame, width=30)
        self.recipient_txt.pack(side="left", fill="x", expand=True, padx=5)

        # Subject
        subject_frame = tk.Frame(form_frame)
        subject_frame.pack(fill="x", pady=2)
        subject_frame.configure(bg="#1E2136")
        tk.Label(subject_frame,bg="#1E2136",text="Subject:").pack(side="left", padx=5)
        self.subject_txt = tk.Entry(subject_frame, width=30)
        self.subject_txt.pack(side="left", fill="x", expand=True, padx=5)

        # Message Content
        tk.Label(form_frame, bg="#1E2136",text="Message:").pack(anchor="w", padx=5)
        self.content_txt = tkst.ScrolledText(form_frame, width=30, height=4, wrap="word")
        self.content_txt.pack(fill="both", expand=True, padx=5, pady=5)

        # Priority
        priority_frame = tk.Frame(form_frame)
        priority_frame.pack(fill="x")
        priority_frame.configure(bg="#1E2136")
        tk.Label(priority_frame,bg="#1E2136", text="Priority (0-5):").pack(side="left", padx=5)
        self.priority_txt = tk.Entry(priority_frame, width=5)
        self.priority_txt.pack(side="left", padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=1)
        btn_frame.configure(bg="#1E2136")
        tk.Button(btn_frame, text="Cancel", command=self.close).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Send", command=self.send).pack(side="left", padx=10)


    @staticmethod
    def validate_email(email):
        """Validates an email address format."""
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email)

    def close(self):
        """Navigates back to the home page instead of destroying the window."""
        self.controller.show_frame(ListMessagesPage)  # Change this to the actual home page class

    def send(self, **kwargs):
        """Handles sending messages.
        """
        sender = self.sender_txt.get().strip()
        subject = self.subject_txt.get().strip()
        recipient = self.recipient_txt.get().strip()
        content = self.content_txt.get("1.0", tk.END).strip()
        priority = self.priority_txt.get().strip()


        # Validate input fields
        if not (sender and recipient and subject and content):
            messagebox.showerror("Error", "All fields must be filled!")
            return

        # Validate emails
        if not self.validate_email(sender) or not self.validate_email(recipient):
            messagebox.showerror("Error", "Invalid email format!")
            self.clearField(self.sender_txt)
            self.clearField(self.recipient_txt)
            return

        # Convert priority to integer
        try:
            priority = int(priority)
            if not (0 <= priority <= 5):
                raise ValueError

        except ValueError:
            messagebox.showerror("Error", "Priority must be between 0 and 5!")
            self.clearField(self.priority_txt)
            return

        # Save message using message_manager
        new_message(sender, recipient, subject, content, "Unread", priority)
        print(f"new_message called with {sender}") #debugging to check if new_message is called
         # Show status
        messagebox.showinfo("Status", "Message was sent successfully!")
        # Clear only specific fields
        self.clearField(self.sender_txt)
        self.clearField(self.recipient_txt)
        self.clearField(self.subject_txt)
        self.clearField(self.content_txt)
        self.clearField(self.priority_txt)

    @staticmethod
    def clearField(field):
        """Clears the content of a given Entry or Text widget."""
        if isinstance(field, tk.Entry):
            field.delete(0, tk.END)
        elif isinstance(field, tkst.ScrolledText):
            field.delete("1.0", tk.END)
