
class Message:
    def __init__(self, sender, recipient,subject,  message, label, priority=0):
        self.sender = sender
        self.subject = subject
        self.recipient = recipient

        self.content = message
        self.label = label
        self.priority = priority
        # self.unread = False

    def info(self):
        return f" {self.stars():8} {self.sender:27} {self.label:10}  {self.subject} \n"


    def stars(self):
        stars = ""
        for i in range(self.priority):
            stars += "*"
        return stars
        # return "*" * self.priority
