import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os

# Configure logging
logging.basicConfig(filename='agent_groq.log', level=logging.INFO)

class GroqAgent:
    def __init__(self, gmail_user, gmail_password):
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password
        self.blacklist = set()
        self.load_blacklist()

    def load_blacklist(self):
        """Load blacklist from a file if it exists."""
        if os.path.exists('blacklist.txt'):
            with open('blacklist.txt', 'r') as file:
                self.blacklist = set(file.read().splitlines())
        logging.info("Blacklist loaded: {}".format(self.blacklist))

    def send_email(self, to_email, subject, body):
        """Send an email via Gmail."""
        if to_email in self.blacklist:
            logging.warning("Attempt to send email to blacklisted address: {}".format(to_email))
            return "Email not sent. Address is blacklisted."
        
        msg = MIMEMultipart()
        msg['From'] = self.gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add unsubscribe link
        unsubscribe_link = f"http://example.com/unsubscribe?email={to_email}"
        body += f"\n\nTo unsubscribe, click here: {unsubscribe_link}"
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            server.sendmail(self.gmail_user, to_email, msg.as_string())
            server.close()
            logging.info("Email sent to: {}".format(to_email))
            return "Email sent successfully!"
        except Exception as e:
            logging.error("Failed to send email to {}: {}".format(to_email, str(e)))
            return "Failed to send email."

    def add_to_blacklist(self, email):
        """Add an email to the blacklist."""
        if email not in self.blacklist:
            self.blacklist.add(email)
            with open('blacklist.txt', 'a') as file:
                file.write(email + '\n')
            logging.info("Email added to blacklist: {}".format(email))

    def automate_prospects(self, prospects):
        """Automate the prospecting process."""
        for prospect in prospects:
            subject = "Hello, {}".format(prospect['name'])
            body = "Dear {},\n\nWe are excited to share our services with you!".format(prospect['name'])
            self.send_email(prospect['email'], subject, body)

# Usage example:
# agent = GroqAgent('your_email@gmail.com', 'your_password')
# agent.automate_prospects([{'email': 'example1@example.com', 'name': 'Customer 1'}, {'email': 'example2@example.com', 'name': 'Customer 2'}])
