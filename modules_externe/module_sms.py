from twilio.rest import Client
from django.conf import settings


def envoyer_message(message, dest):
    # Initialiser le client Twilio
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # Envoyer le message
    message = client.messages.create(
            body=message,
            from_='+18159348590', 
            to=dest
        )
    return message