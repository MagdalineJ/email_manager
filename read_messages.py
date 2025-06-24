
import tkinter as tk
from tkinter import messagebox
import message_manager as messages  # Custom module for managing messages
from list_messages import ListMessagesPage


class ReadMessagesPage(tk.Frame):
    def __init__(self, parent, controller, message_id):
        super().__init__(parent) #parent tkinter widget
        self.controller = controller #refrence to the main application controller for navigation
        self.message_id = message_id  # Store message ID
        # Set background color for the frame
        self.config(bg="#1E2136")
        # title label for the page
        tk.Label(self, bg="#1E2136",text=f"Reading Message no {message_id}", font=("Bold", 18)).pack(pady=10)

        # Validate and fetch message data
        self.message = messages.get_message_by_id(self.message_id)

        # handling if the message id doesn't exist
        if not self.message:
            self.controller.show_frame(ListMessagesPage)
            return

        """Creates the UI elements for displaying message details."""
        # Create a frame for the label and entry to be side by side
        container = tk.Frame(self)
        container.configure(bg="#1E2136")
        container.pack(padx=10, pady=10, fill="both", expand=True)

        # Update status label
        if hasattr(self.master.master, "status_lbl"):
            self.master.master.status_lbl.config(text="Read Message \n\n button was clicked!")

        # From field
        from_frame = tk.Frame(container)
        from_frame.pack(fill="x", padx=10 ,pady=2)

        tk.Label(from_frame, text="From:    ").pack(side="left", padx=5)
        self.sender_txt = tk.Entry(from_frame, width=24, readonlybackground='#d9d9d9', fg='#000000')
        self.sender_txt.pack(side="left", fill="x", expand=True, padx=5)
        self.sender_txt.insert(tk.END, self.message.sender)
        self.sender_txt.configure(state="readonly")

        # To field
        to_frame = tk.Frame(container)
        to_frame.pack(fill="x",padx=10, pady=2)

        tk.Label(to_frame, text="To:        ").pack(side="left", padx=5)
        self.recipient_txt = tk.Entry(to_frame, width=24,readonlybackground='#d9d9d9', fg='#000000')
        self.recipient_txt.pack(side="left", fill="x", expand=True, padx=5)
        self.recipient_txt.insert(tk.END, self.message.recipient)
        self.recipient_txt.configure(state="readonly")

        # Subject field
        subject_frame = tk.Frame(container)
        subject_frame.pack(fill="x",padx=10, pady=2)

        tk.Label(subject_frame, text="Subject:").pack(side="left", padx=5)
        self.subject_txt = tk.Entry(subject_frame, width=24,readonlybackground='#d9d9d9', fg='#000000')
        self.subject_txt.pack(side="left", fill="x", expand=True, padx=5)
        self.subject_txt.insert(tk.END, self.message.subject)
        self.subject_txt.configure(state="readonly")

        # Message field (multi-line text box)
        message_frame = tk.Frame(container)
        message_frame.pack(fill="x",padx=10,pady=2)

        tk.Label(message_frame, text="Message:").pack(side="left", padx=5)
        self.content_txt = tk.Text(message_frame, width=40, height=6, wrap="word")
        self.content_txt.pack(side="left", fill="x", expand=True, padx=5)
        self.content_txt.insert(tk.END, self.message.content)
        self.content_txt.configure(state="disabled")

        # Priority field
        priority_frame = tk.Frame(container)
        priority_frame.pack(fill="x", padx=10, pady=2)
        priority_frame.configure(bg="#1E2136")

        tk.Label(priority_frame,bg="#1E2136", text="New Priority (1-5):").pack(side="left", padx=5)
        self.priority_txt = tk.Entry(priority_frame, width=5)
        self.priority_txt.pack(side="left", padx=5)

        # Buttons (Update, Delete, Close)
        button_frame = tk.Frame(container)
        button_frame.pack(pady=10)
        button_frame.configure(bg="#1E2136")
        update_btn = tk.Button(button_frame, text="Update", command=self.update_priority)
        update_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(button_frame, text="Delete", command=self.delete_message)
        delete_btn.pack(side="left", padx=5)

        close_btn = tk.Button(button_frame, text="Close", command=self.close)
        close_btn.pack(side="left", padx=5)



    def update_priority(self):
        """Updates the priority of the message."""
        try:
            priority = int(self.priority_txt.get()) #get input form user
            if 1 <= priority <= 5:
                messages.set_priority(self.message_id, priority)  #update priority
                messagebox.showinfo("Success", "Priority updated!") #success message
                self.clear()
            else:
                messagebox.showwarning("Invalid Input", "Priority must be between 1 and 5") #error message
                self.clear()

        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number between 1 and 5.") #error message
            self.clear()

    def delete_message(self):
        """Deletes the selected message."""
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this message?"):
            messages.delete_message(self.message_id)
            messagebox.showinfo("Deleted", "Message has been deleted.")
            self.close()

    def close(self):  # closes the gui window when called
        self.controller.show_frame(ListMessagesPage)

    def clear(self):
        self.priority_txt.delete(0, tk.END)  # clears input field for priority
