import email, smtplib, ssl
from providers import PROVIDERS

def send(num_list,message):
    import email, smtplib, ssl
    from providers import PROVIDERS
    for n in num_list:
        number = n[0]
        provider = n[1]
        receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'
        subject = "/",
        sender_email = '4806BrierRose@brenesfinancial.com'
        email_password = 'M0n3yH0m3'

        email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=ssl.create_default_context()
        ) as email:
            email.login(sender_email, email_password)
            email.sendmail(sender_email, receiver_email, email_message)    