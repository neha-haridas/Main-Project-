from django.conf import settings
# from .models import Leave
import twilio
import twilio.rest

def send_twilio_message(parents_contact, body):
    client = twilio.rest.TwilioRestClient(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    return client.messages.create(
        body=body,
        to=parents_contact,
        from_=settings.TWILIO_PHONE_NUMBER
    )

