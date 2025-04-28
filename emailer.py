import os
import smtplib
import datetime
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_FROM = os.getenv("EMAIL_FROM")
TO_EMAIL = os.getenv("TO_EMAIL")
SUMMARIES_DIR = "summaries"

def load_summary(date=None):
    if date is None:
        date = datetime.date.today()

    filename = os.path.join(SUMMARIES_DIR, f"dailyUpdate_{date.isoformat()}.html")

    if not os.path.exists(filename):
        print(f"No summary found for {date.isoformat()}")
        return None, None

    with open(filename, "r", encoding="utf-8") as f:
        summary_html = f.read()

    file_creation_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))

    return summary_html, file_creation_time

def send_email(subject, plain_body, html_body):
    msg = EmailMessage()
    msg['From'] = EMAIL_FROM
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.set_content(plain_body)
    msg.add_alternative(html_body, subtype='html')

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(msg)

    print("Email sent successfully.")

def main():
    summary_html, creation_time = load_summary()

    if not summary_html:
        return

    today_date = datetime.date.today()
    today_str_subject = today_date.strftime("%d.%m.%Y")
    creation_time_str = creation_time.strftime("%d.%m.%Y %H:%M")

    # Email subject
    subject = f"USUAL summary bot: {today_str_subject}"

    # Plain body fallback (minimal)
    plain_body = f"Hey, Mario!\nToday's update of the USUAL general chat.\n\nReport created at: {creation_time_str}\n\n(This email contains an HTML formatted report.)"

    # Full HTML email
    html_body = f"""
    <html>
        <body>
            <p>Hey, Mario! 👋<br>
            Today's update of the <b>USUAL general chat</b>.</p>
            <p>Report created at: {creation_time_str}</p>
            <hr>
            {summary_html}
        </body>
    </html>
    """

    send_email(subject, plain_body, html_body)

if __name__ == "__main__":
    main()
