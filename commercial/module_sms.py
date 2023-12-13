from twilio.rest import Client
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def envoyer_message(message, *dest):
    # Initialiser le client Twilio
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Liste pour stocker les destinataires ayant réussi l'envoi
    destinataires_reussis = []

    # Envoyer le message à chaque destinataire
    for destinataire in dest:
        try:
            message_envoye = client.messages.create(
                body=message,
                from_='+18159348590',  # Votre numéro Twilio ici
                to=destinataire
            )
            print(f"Message envoyé à {destinataire}: {message_envoye.sid}")
            destinataires_reussis.append(destinataire)
        except TwilioRestException as e:
            print(f"Erreur lors de l'envoi du message à {destinataire}: {str(e)}")

    return destinataires_reussis

