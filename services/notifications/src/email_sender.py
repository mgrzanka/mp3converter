from email.message import EmailMessage
import smtplib

from src.config import Config

class EmailSender:
    def send_email(self, message):
        mp3_fid = message["mp3_fid"]
        user_email = message["email"]
        dowload_url = f"{Config.MP3_DOWLOAD_ENDPOINT}?mp3_fid={mp3_fid}"

        email_message = EmailMessage()
        email_message.set_content(f"Your mp3 file is ready. Download it from {dowload_url}. Remember to add JWT token.")
        email_message["Subject"] = "MP3 DOWNLOAD"
        email_message["FROM"] = Config.SENDER_EMAIL
        email_message["TO"] = user_email

        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(Config.SENDER_EMAIL, Config.SENDER_EMAIL_PASSWORD)
        session.send_message(email_message)
        session.quit()
