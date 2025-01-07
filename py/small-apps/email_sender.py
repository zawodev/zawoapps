import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# konfiguracja nadawcy, odbiorcy i serwera
sender_email = "test@gmail.com"
password = "code here"
receiver_email = "test@gmail.com"

# tworzenie wiadomości z polskimi znakami
subject = "Automatyczny mail python"
body = "Cześć! Ta wiadomość testowa została wysłana przez python - z polskimi znakami: ą, ć, ę, ł, ń, ó, ś, ź, ż."

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# dodanie treści do wiadomości
message.attach(MIMEText(body, "plain", "utf-8"))

# wysyłanie e-maila
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # szyfrowanie połączenia
        server.login(sender_email, password)  # logowanie do serwera SMTP
        server.sendmail(sender_email, receiver_email, message.as_string())  # wysłanie wiadomości
    print("E-mail został wysłany!")
except Exception as e:
    print(f"Wystąpił błąd: {e}")
