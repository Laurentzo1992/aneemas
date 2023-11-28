from twilio.rest import Client
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def envoyer_message(message, *dest):
    # Initialiser le client Twilio
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Variable pour stocker les résultats de l'envoi
    result_list = []

    # Envoyer le message à chaque destinataire
    for destinataire in dest:
        try:
            message_envoye = client.messages.create(
                body=message,
                from_='+18159348590',
                to=destinataire
            )
            print(f"Message envoyé à {destinataire}: {message_envoye.sid}")
            result_list.append(f"Message envoyé à {destinataire}")
        except TwilioRestException as e:
            print(f"Erreur lors de l'envoi du message à {destinataire}: {str(e)}")
            result_list.append(f"Erreur lors de l'envoi du message à {destinataire}")

    # Retourner le résultat global
    return result_list


