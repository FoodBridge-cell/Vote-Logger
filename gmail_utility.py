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
        raw_email = msg_data[0][1]

        # Try decoding with multiple encodings
        for encoding in ["utf-8", "ISO-8859-1"]:
            try:
                decoded_email = raw_email.decode(encoding)
                break
            except UnicodeDecodeError:
                decoded_email = None

        if not decoded_email:
            raise Exception("Failed to decode email content")

        email_message = email.message_from_string(decoded_email)

        # Extract OTP from the email body
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":  # Extract plain text content
                for encoding in ["utf-8", "ISO-8859-1"]:
                    try:
                        body = part.get_payload(decode=True).decode(encoding, errors="replace")
                        break
                    except UnicodeDecodeError:
                        body = None

                if body:
                    otp = extract_otp_from_body(body)
                    if otp:
                        return otp
                    else:
                        raise Exception("OTP not found in the email body")
                else:
                    raise Exception("Failed to decode email body")

    except Exception as e:
        print(f"Error fetching OTP: {e}")

    finally:
        mail.logout()

def extract_otp_from_body(body):
    """Extract the OTP from the email body."""
    import re
    # Regex to find a 6-digit OTP
    otp_match = re.search(r"Your OTP for event registration is:\s*(\d{7})", body)
    return otp_match.group(1) if otp_match else None
