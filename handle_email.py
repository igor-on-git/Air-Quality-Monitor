import smtplib
from email.mime.text import MIMEText
from email_credentials import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

def send_email(body):
        # Email Configuration
        SMTP_SERVER = "smtp.gmail.com"  # For Gmail (use different SMTP for other providers)
        SMTP_PORT = 587  # TLS port

        # Prepare the email message
        subject = "AQI Notification"
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        #msg["To"] = ", ".join(EMAIL_RECEIVERS)  # Convert list to a string

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print("Notification email sent successfully!")