import imaplib
import email
from config import GMAIL_USERNAME, GMAIL_PASSWORD

def fetch_otp():
    """Fetch the latest OTP email from the Gmail inbox."""
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        mail.select("inbox")

        # Search for emails containing OTP (adjust sender if needed)
        status, messages = mail.search(None, 'FROM "challenge@mastersunion.org"')  # Replace with the actual sender email
        messages = messages[0].split()

        if not messages:
            raise Exception("No OTP email found")

        # Fetch the latest email
        latest_email = messages[-1]
        status, msg_data = mail.fetch(latest_email, "(RFC822)")
        raw_email = msg_data[0][1].decode("utf-8")
        email_message = email.message_from_string(raw_email)

        # Extract OTP from the email body
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode("utf-8")
                otp = extract_otp_from_body(body)
                if otp:
                    return otp
                else:
                    raise Exception("OTP not found in the email body")

    except Exception as e:
        print(f"Error fetching OTP: {e}")

    finally:
        mail.logout()

def extract_otp_from_body(body):
    """Extract the OTP from the email body using regex."""
    import re
    otp_match = re.search(r'\b\d{6}\b', body)  # Assuming OTP is a 6-digit number
    return otp_match.group(0) if otp_match else None
