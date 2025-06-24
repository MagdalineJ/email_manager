import tkinter as tk
from tkinter import messagebox
import message_manager as messages  # Handles message storage and retrieval
from list_messages import ListMessagesPage


class LabelMessagesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Reference to EmailManagerApp
        # Set background color for the frame
        self.config(bg="#1E2136")
        tk.Label(self,bg="#1E2136", text="Label Messages", font=("Bold", 18)).pack(pady=10)

        # Label Selection
        label_frame = tk.Frame(self)
        label_frame.pack(pady=5)
        label_frame.configure(bg="#1E2136")
        tk.Label(label_frame,bg="#1E2136", text="Select Label:").pack(side="left", padx=5)

        self.label_var = tk.StringVar()
        self.label_dropdown = tk.OptionMenu(label_frame, self.label_var, "Read", "Unread", "Work", "Personal",
                                            "To Follow Up", "Important", "Flagged", "Scam")
        self.label_dropdown.pack(side="left", padx=5)

        # Button to List Messages by Label
        tk.Button(self, text="List Messages", command=self.list_labelled_messages).pack(pady=5)

        # Text Box to Display Messages
        self.list_txt = tk.Text(self,bg="#1E2136", width=65, height=15, wrap="none", state="disabled")
        self.list_txt.pack(pady=5)

        # Message ID Input for Adding Labels
        msg_frame = tk.Frame(self)
        msg_frame.pack(pady=5)
        msg_frame.configure(bg="#1E2136")
        tk.Label(msg_frame,bg="#1E2136", text="Message ID:").pack(side="left", padx=5)

        self.msg_id_txt = tk.Entry(msg_frame,width=5)
        self.msg_id_txt.pack(side="left", padx=5)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=1)
        btn_frame.configure(bg="#1E2136")
        tk.Button(btn_frame,text="Add Label", command=self.add_label_to_message).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Back", command=self.back).pack(side="left", padx=10)

        # Update EmailManagerApp status label safely
        if hasattr(self.controller, "status_lbl") and self.controller.status_lbl:
            self.controller.status_lbl.config(text=f"Label messages \n\nbutton was clicked", font=('Bold', 12))

    def list_labelled_messages(self):
        label = self.label_var.get()
        if not label:
            messagebox.showerror("Error", "Please select a label.")
            return
        message_list = messages.list_all(label)

        if  label not in message_list:
            messagebox.showerror("Empty List", "No Messages Found!")
            # print(f"message with {label}label not found")
            self.list_txt.config(state=tk.NORMAL)  # Enable editing
            self.list_txt.delete("1.0", tk.END)  # Clear existing text
            self.list_txt.insert(tk.END,f"\n No messages found with the {label} label.\n\n Try selecting a different label! 😊") # Insert new text
            self.list_txt.config(state=tk.DISABLED)  # Make it read-only again
            self.controller.status_lbl.config(text=f"No messages \n\n  labeled as {label}")

            return

        # Convert list of messages into formatted text
        formatted_messages = "".join(message_list)

        self.list_txt.config(state="normal")  # Enable text area
        self.list_txt.delete("1.0", tk.END)  # Clear previous content
        self.list_txt.insert("1.0", formatted_messages)  # Insert messages
        self.list_txt.config(state="disabled")  # Disable to prevent user edits

        if hasattr(self.controller, "status_lbl") and self.controller.status_lbl:
            self.controller.status_lbl.config(text=f"Showing messages \n\n  labeled as {label}")


    def add_label_to_message(self):
        """Assigns a label to a specific message."""
        label = self.label_var.get()
        message_id = self.msg_id_txt.get().strip()

        if not label:
            messagebox.showerror("Error", "Please select a label.")
            return

        if not message_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid message ID.")
            self.clear()
            return

        message_id = int(message_id)

        # Correct way to check if message exists
        if message_id not in messages.messages:
            messagebox.showerror("Error", "Message ID not found.")
            self.clear()
            return

        messages.set_label(message_id, label)  # Apply label to message
        messagebox.showinfo("Success", f"Label '{label}' added to message {message_id}.")
        self.clear()

    def back(self):
        """Navigates back to the home page instead of destroying the window."""
        self.controller.show_frame(ListMessagesPage)  # Change this to the actual home page class

    def clear(self):
        self.msg_id_txt.delete(0, tk.END) #clear msg ID field
