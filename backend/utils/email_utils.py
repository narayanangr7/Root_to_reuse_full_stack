import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path

# Load .env from backend directory explicitly
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Email Configuration - strip whitespace/quotes to avoid hidden chars
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip().strip('"').strip("'")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "").strip().strip('"').strip("'")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").strip().strip('"').strip("'")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER).strip().strip('"').strip("'")

# Debug: Print loaded credentials at startup (masked password)
print(f"[EMAIL CONFIG] .env path: {env_path} (exists: {env_path.exists()})")
print(f"[EMAIL CONFIG] SMTP_SERVER: '{SMTP_SERVER}'")
print(f"[EMAIL CONFIG] SMTP_PORT: {SMTP_PORT}")
print(f"[EMAIL CONFIG] SMTP_USER: '{SMTP_USER}'")
print(f"[EMAIL CONFIG] SMTP_PASSWORD: '{SMTP_PASSWORD[:4]}****' (length: {len(SMTP_PASSWORD)})")
print(f"[EMAIL CONFIG] FROM_EMAIL: '{FROM_EMAIL}'")

def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using SMTP.
    If credentials are missing on Vercel, it returns False.
    On local, it prints to console (Mock mode).
    """
    is_vercel = os.getenv("VERCEL") == "1"
    
    if not SMTP_USER or not SMTP_PASSWORD:
        if is_vercel:
            print("[ERROR] SMTP credentials missing in Vercel environment variables!")
            return False
        
        print("\n" + "="*50)
        print("MOCK EMAIL SENT (Local Environment)")
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

        # Ports to try: 465 (SSL, usually unblocked) then 587 (STARTTLS)
        ports_to_try = [465, 587]
        
        # If the user explicitly set a different port, try that first
        if SMTP_PORT not in ports_to_try and SMTP_PORT != 0:
            ports_to_try.insert(0, SMTP_PORT)

        # Remove duplicates
        ports_to_try = list(dict.fromkeys(ports_to_try))

        success = False
        last_error = "No ports attempted"

        for port in ports_to_try:
            try:
                print(f"[DEBUG] SMTP: Attempting port {port} on {SMTP_SERVER}...")
                
                if port == 465:
                    # Pure SSL
                    server = smtplib.SMTP_SSL(SMTP_SERVER, port, timeout=4)
                else:
                    # Normal or STARTTLS
                    server = smtplib.SMTP(SMTP_SERVER, port, timeout=4)
                    if port == 587:
                        server.starttls()
                
                server.login(SMTP_USER, SMTP_PASSWORD)
                # Use sendmail for wider compatibility with older smtplib versions if needed
                server.sendmail(FROM_EMAIL, to_email, msg.as_string())
                server.quit()
                
                print(f"[SUCCESS] Email sent to {to_email} via port {port}")
                success = True
                break
            except Exception as e:
                last_error = str(e)
                print(f"[WARNING] SMTP attempt via port {port} failed: {last_error}")
                continue

        if not success:
            print(f"[ERROR] All SMTP ports failed. Last error: {last_error}")
        return success

    except Exception as e:
        print("\n" + "!"*50)
        print(f"CRITICAL EMAIL FAILURE: {str(e)}")
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
