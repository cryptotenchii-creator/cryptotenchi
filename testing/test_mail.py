# ===========================
# TEST CASE: MANUAL EMAIL TRIGGER (SMTP VERSION)
# ===========================
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")            # your Gmail address
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # your Gmail App Password --> Google Account > Security > App Passwords


def test_manual_reminder():
    """
    Manual trigger to test reminder email sending functionality using SMTP.
    This ignores threshold and last sent checks.
    """
    remaining_videos_count = 5  # You can set any number for test
    print(f"[TEST] Sending manual reminder for {remaining_videos_count} remaining videos...")

    try:
        subject = "[TEST] Video Processing Reminder"
        body = f"[TEST] You have {remaining_videos_count} unprocessed videos remaining. This is a manual test."

        # Compose email
        msg = MIMEText(body)
        msg["From"] = GMAIL_USER
        msg["To"] = GMAIL_USER
        msg["Subject"] = subject

        # Send email via SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, APP_PASSWORD)
            server.send_message(msg)
        
        print("[TEST ✅] Reminder email sent successfully!")

        # Optionally, update Google Sheet here if needed
        # update_reminder_date(sheet_video_name, datetime.datetime.now().isoformat())

    except Exception as e:
        print(f"[TEST ❌] Failed to send test reminder: {e}")


# ===========================
# Run test manually
# ===========================
if __name__ == "__main__":
    test_manual_reminder()
