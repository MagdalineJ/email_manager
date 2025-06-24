import csv
import os
from message import Message

MESSAGES_FILE = "messages.csv"  # CSV file name
HEADERS = ["id", "sender", "recipient", "subject","message","label","priority"]


def initialize_csv():
    """Creates CSV file with default messages if it doesn't exist."""
    if not os.path.exists(MESSAGES_FILE) or os.stat(MESSAGES_FILE).st_size == 0:
        with open(MESSAGES_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
        print("CSV file initialized.")

    existing_messages = load_messages()
    messages.update(existing_messages)
    save_all_messages(messages)


def load_messages():
    """Loads messages from CSV into a dictionary (message_id: Message)."""
    loaded_messages = {}
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Ensure priority is a valid integer, otherwise default to 0
                    try:
                        # priority = int(row.get("priority", 0))  # Default to 0 if invalid
                        priority = int(row["priority"])
                    except ValueError:
                        priority = 0  # If conversion fails, set priority to 0

                    loaded_messages[int(row["id"])] = Message(
                        row["sender"],
                        row["recipient"],
                        row["subject"],
                        row["message"],
                        row.get("label", "Unread"),  # Ensure label is always set
                        priority  # Use the safely parsed priority
                    )
        except Exception as e:
            print(f"Error loading messages: {e}")
    return loaded_messages


def save_all_messages(messages):
    """Overwrites the CSV file with the given messages dictionary."""
    try:
        with open(MESSAGES_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
            for msg_id, msg in messages.items():
                writer.writerow([msg_id, msg.sender, msg.recipient,msg.subject, msg.content,msg.label,msg.priority])
    except Exception as e:
        print(f"Error saving messages: {e}")


messages = load_messages()  # Ensure messages dictionary is always up-to-date


def list_all(label=None):
    output = "ID Priority  From                        label       Subject\n" \
             "== ========  ====                        =====       =======\n"
    for message_id, message in messages.items():
        # if label is not None and (len(label) == 0 or label not in message.label):
        #     continue
        if label and label not in message.label:
            continue
        # output += f"{message_id:2d} {message.priority:8d} {message.sender:25} {message.subject}\n"
        output += f"{message_id:2d} {message.info()}"

    return output


# def get_sender(message_id):
def get_message_by_id(message_id):
    return messages.get(message_id, None)

def get_priority(message_id):
    # return messages.get(message_id, -1)
    try:
        message = messages[message_id]
        return message.priority
    except KeyError:
        return -1

def set_priority(message_id, priority):
    try:
        if message_id in messages:
            messages[message_id].priority = priority
            save_all_messages(messages)
    except KeyError:
        return


def set_label(message_id, label):
    if message_id in messages:
        messages[message_id].label = label
        save_all_messages(messages)


def delete_message(message_id):
    if message_id in messages:
        messages.pop(message_id)
        save_all_messages(messages)


def new_message(sender,recipient, subject,  content,label, priority):
    """Creates a new message and assigns a unique ID."""
    message_id = max(messages.keys(), default=0) + 1

    messages[message_id] = Message(sender,recipient,subject,content,label, priority)
    save_all_messages(messages)
