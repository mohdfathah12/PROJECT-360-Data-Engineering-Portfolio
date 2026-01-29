import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert(subject, body, to_emails):
    # Email configuration
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"  # Use app password for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Build message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_emails, msg.as_string())
        server.quit()
        print("✅ Alert sent successfully")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")


# Example usage
if __name__ == "__main__":
    send_alert(
        "DE Project Alert",
        "Silver layer job failed! Please check logs.",
        ["client@example.com"]
    )
