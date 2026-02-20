import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using SMTP.
    If credentials are missing, it just prints the email to console (Mock mode).
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        print("\n" + "="*50)
        print("MOCK EMAIL SENT (Credentials missing in .env)")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print("="*50 + "\n")
        return True

    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Try SSL on port 465 first (more firewall-friendly)
        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, 465, timeout=10) as server:
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
            print(f"Email sent successfully to {to_email} via SSL (port 465)")
            return True
        except Exception as ssl_err:
            print(f"SSL attempt failed: {ssl_err}. Trying STARTTLS on port 587...")

        # Fallback: Try STARTTLS on port 587
        with smtplib.SMTP(SMTP_SERVER, 587, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully to {to_email} via STARTTLS (port 587)")
        return True

    except Exception as e:
        print("\n" + "!"*50)
        print(f"EMAIL ERROR: Failed to send email to {to_email}")
        print(f"Details: {str(e)}")
        print("!"*50 + "\n")
        return False

def send_volunteer_approval_email(to_email: str, name: str):
    subject = "Volunteer Application Approved - Root to Reuse"
    body = f"Hello {name},\n\nCongratulations! Your application to become a volunteer at Root to Reuse has been approved by the admin.\n\nYou can now propose and join camping events to help our mission.\n\nBest regards,\nThe Root to Reuse Team"
    return send_email(to_email, subject, body)

def send_camp_approval_email(to_email: str, name: str, event_name: str):
    subject = "Camp Proposal Approved - Root to Reuse"
    body = f"Hello {name},\n\nYour camp proposal '{event_name}' has been reviewed and approved by the admin!\n\nIt is now live on our events page for other volunteers to join.\n\nBest regards,\nThe Root to Reuse Team"
    return send_email(to_email, subject, body)

def send_camp_joined_email(to_email: str, name: str, event_name: str, organizer_name: str):
    subject = f"Joined Event: {event_name} - Root to Reuse"
    body = f"Hello {name},\n\nYou have successfully joined the event '{event_name}' organized by {organizer_name}.\n\nThank you for your contribution to the Karuvela removal campaign!\n\nBest regards,\nThe Root to Reuse Team"
    return send_email(to_email, subject, body)
