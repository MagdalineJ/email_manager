import tkinter as tk
from tkinter import messagebox #messagebox for displaying alerts
import font_manager as fonts # Manages fonts
from list_messages import ListMessagesPage
from read_messages import ReadMessagesPage
from new_message import NewMessagePage
from label_messages import LabelMessagesPage


class EmailManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.status_lbl = None
        self.geometry('700x500')
        self.title('Email Manager')

        # Sidebar Frame (Navigation)
        self.options_frame = tk.Frame(self, bg='#7393B3', width=190, height=400)
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.options_frame.pack_propagate(False)

        # Main content frame (for switching pages)
        self.main_frame = tk.Frame(self, bg='#1E2136',width=450, height=400)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_frame.pack_propagate(False)

        # Sidebar Buttons
        self.create_sidebar()

        # Show the default frame
        self.show_frame(ListMessagesPage)

    # --------------------------------------------
    def show_frame(self, page_class):
        """Switches to the selected page by creating a new instance."""

        # Retrieve message ID before destroying widgets (if required)
        if page_class == ReadMessagesPage:
            message_id = self.id_txt.get().strip()  # Get message ID from entry
            if not message_id.isdigit():
                tk.messagebox.showerror("Error", "Please enter a valid Message ID.")
                self.id_txt.delete(0, tk.END)  # clear invalid entry

                return  # Prevents loading an invalid page
            message_id = int(message_id)
            self.id_txt.delete(0, tk.END)  # Clear entry after retrieval

        else:
            message_id = None  # Other pages don’t use message_id

        # Destroy old page
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Ensure valid instance creation
        try:
            if page_class == ReadMessagesPage and message_id is not None:
                frame = page_class(self.main_frame, self, message_id)  # Pass message_id
            else:
                frame = page_class(self.main_frame, self)  # Other pages

            frame.pack(fill=tk.BOTH, expand=True, pady=20)  # Ensure valid packing

            # If the page has a list_messages method, call it
            if hasattr(frame, "list_messages"):
                frame.list_messages()
        except:
            messagebox.showerror("Error", f"Message {message_id} not found!")

    # --------------------------------------------
    def create_sidebar(self):
        """Creates sidebar navigation with buttons."""
        self.list_message_indicator = tk.Label(self.options_frame, text='', bg='#7393B3')
        self.list_message_indicator.place(x=14, y=15, width=5, height=38)

        list_messages_btn = tk.Button(self.options_frame, text="List Messages", font=('Bold', 12), fg="#1155cc",
                                      bd=0, bg='#7393B3', width=15, height=2,
                                      command=lambda: self.indicate(self.list_message_indicator, ListMessagesPage))
        list_messages_btn.pack(pady=15)

        self.read_message_indicator = tk.Label(self.options_frame, text='', bg='#7393B3')
        self.read_message_indicator.place(x=17, y=83, width=5, height=38)

        read_frame = tk.Frame(self.options_frame, bg='#7393B3')
        read_frame.pack(pady=15)

        read_message_btn = tk.Button(read_frame, text="Read Message:", font=('Bold', 12), fg="#1155cc", bd=0,
                                     bg='#7393B3', width=10, height=2,
                                     command=lambda: self.indicate(self.read_message_indicator, ReadMessagesPage))
        read_message_btn.pack(side=tk.LEFT)

        self.id_txt = tk.Entry(read_frame, width=2)
        self.id_txt.pack(side=tk.LEFT, padx=2)

        self.new_message_indicator = tk.Label(self.options_frame, text='', bg='#7393B3')
        self.new_message_indicator.place(x=14, y=151, width=5, height=38)

        new_message_btn = tk.Button(self.options_frame, text="New Message", font=('Bold', 12), fg="#1155cc", bd=0,
                                    bg='#7393B3', width=15, height=2,
                                    command=lambda: self.indicate(self.new_message_indicator, NewMessagePage))
        new_message_btn.pack(pady=15)

        self.label_message_indicator = tk.Label(self.options_frame, text='', bg='#7393B3')
        self.label_message_indicator.place(x=14, y=219, width=5, height=38)

        label_messages_btn = tk.Button(self.options_frame, text="Label Messages", font=('Bold', 12), fg="#1155cc", bd=0,
                                       bg='#7393B3', width=15, height=2,
                                       command=lambda: self.indicate(self.label_message_indicator, LabelMessagesPage))
        label_messages_btn.pack(pady=15)



        # Status Label (Shared by all pages)
        self.status_lbl = tk.Label(self.options_frame, text="",
                                   bg="#7393B3", fg="#1E2136")
        self.status_lbl.pack(side="bottom", fill="x", pady=20)  # Ensure it's at the bottom of sidebar

    # -----------------------------------------
    def hide_indicator(self):
        """Resets all sidebar indicators."""
        self.list_message_indicator.config(bg='#7393B3')
        self.read_message_indicator.config(bg='#7393B3')
        self.new_message_indicator.config(bg='#7393B3')
        self.label_message_indicator.config(bg='#7393B3')

    # -----------------------------------------
    def indicate(self, indicator, page_class):
        """Highlights active section and refreshes frame."""
        self.hide_indicator()
        indicator.config(bg='#1155cc')
        self.show_frame(page_class)

# -------- Run the App ---------
if __name__ == "__main__":
    app=EmailManagerApp()
    fonts.configure()  # configure the fonts
    app.mainloop()