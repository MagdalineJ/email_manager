import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.scrolledtext as tkst
import message_manager as messages


class ListMessagesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Set background color for the frame
        self.configure(bg="#1E2136")

        # Label for "All Messages"
        self.label = tk.Label(self,bg="#1E2136", text="All Messages", font=("Bold", 18))
        self.label.pack(pady=10)

        # Filter Row (Dropdown + Entry + Button on the same line)
        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)
        filter_frame.configure(bg="#1E2136")
        tk.Label(filter_frame, bg="#1E2136",text="Filter by:").pack(side="left", padx=3)

        self.filter_option = ttk.Combobox(filter_frame, values=["Sender", "Recipient", "Subject", "Message"],
                                          state="readonly", width=8)
        self.filter_option.pack(side="left", padx=5)
        self.filter_option.current(0)

        self.filter_entry = tk.Entry(filter_frame, width=10)
        self.filter_entry.pack(side="left", padx=5)
        self.filter_entry.bind("<KeyRelease>", self.toggle_search_button)  # Enable/Disable button dynamically

        self.search_button = tk.Button(filter_frame, text="Search", command=self.filter_messages, state="disabled")
        self.search_button.pack(side="left", padx=5)

        self.refresh_button = tk.Button(filter_frame, text="Refresh", command=self.refresh)
        self.refresh_button.pack(side="left", padx=5)

        # Scrolled text widget to display messages
        self.list_txt = tkst.ScrolledText(self,bg="#1E2136", width=75, height=18, wrap="none")
        self.list_txt.pack(padx=10, pady=10)

    def toggle_search_button(self, event=None):
        """Enables/disables the search button based on input."""
        search_value = self.filter_entry.get().strip()
        self.search_button["state"] = "normal" if search_value else "disabled"

    def list_messages(self):
        """Displays all messages."""
        message_list = messages.list_all()
        set_text(self.list_txt, message_list)

        if hasattr(self.master.master, "status_lbl"):
            self.master.master.status_lbl.config(text="List Messages\n\n button was clicked!")

    def filter_messages(self):
        """Filters messages based on the selected criteria."""
        filter_type = self.filter_option.get()  # Dropdown value (e.g., "Sender", "Label", "Message Content")
        search_value = self.filter_entry.get().strip().lower()

        if not search_value:
            messagebox.showwarning("Invalid Input", "Please enter a value to filter by.")
            return

        filtered_messages = "ID  Priority  From                    Labels           Subject\n"
        filtered_messages += "==  ========  ====                    ======           =======\n"

        matches = []

        for message_id, message in messages.messages.items():
            if filter_type == "Sender":
                field_value = message.sender.lower()
            elif filter_type == "Recipient":
                field_value = message.recipient.lower()
            elif filter_type == "Subject":
                field_value = message.subject.lower()
            elif filter_type == "Priority":
                field_value = str(message.priority)  # Convert number to string for comparison
            elif filter_type == "Label":
                field_value = ", ".join(message.label).lower()  # Join multiple labels as a string
            elif filter_type == "Message":  # Check message body!
                field_value = message.content.lower()
            else:
                messagebox.showwarning("Invalid Filter", "Please select a valid filter type.")
                return

            if search_value in field_value:
                matches.append(f"{search_value} found in {filter_type} {message_id}.")
                filtered_messages += f"{message_id:2d} {message.info()}"

        if not matches:
            self.list_messages()
            messagebox.showwarning("No Matches", f"No messages found for '{search_value}' under '{filter_type}'.")
        else:
            set_text(self.list_txt, filtered_messages)
            messagebox.showinfo("Filtered Messages", "\n".join(matches))

        self.filter_entry.delete(0, tk.END)
        self.toggle_search_button()  # Disable search if empty after filtering

    def refresh(self):
        self.controller.show_frame(ListMessagesPage)  # display all messages as a refresh


def set_text(text_area, content):
    """Sets text inside a text area widget."""
    text_area["state"] = "normal"
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", content if content else "No messages available.")
    text_area["state"] = "disabled"