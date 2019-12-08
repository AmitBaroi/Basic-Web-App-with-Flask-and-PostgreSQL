import smtplib
from email.mime.text import MIMEText


def send_mail(customer, dealer, rating, comments):
    sender_email = 'webapp@example.com'
    receiver_email = 'receiver@example.com'

    host = 'smtp.mailtrap.io'
    port = 2525
    user_name = 'c0ece7179608e4'
    password = '7ce303bd5a834b'
    message = f'<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>'

    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Feedback received'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Sending email
    with smtplib.SMTP(host, port) as server:
        server.login(user_name, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())