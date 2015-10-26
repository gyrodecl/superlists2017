import sys
import requests

import logging
logger = logging.getLogger(__name__)
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'
#DOMAIN = '127.0.0.1:8000'

class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
        logging.warning('entering authenticate function')

        #send the assertion to Mozilla's verifier service.
        data = {'assertion': assertion, 'audience': settings.DOMAIN}
        #print('sending data to mozilla', data, file=sys.stderr)
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={'assertion': assertion, 'audience': settings.DOMAIN}
        )
        logging.warning('got response from persona')
        logging.warning(response.content.decode())
        
        if response.ok and response.json()['status'] =='okay':
            user_email = response.json()['email']
            try:
                return User.objects.get(email=user_email)
            except User.DoesNotExist:
                return User.objects.create(email=user_email)
        else:
            logger.warning(
                'Persona says no. Json was: {}'.format(response.json)   
            )
    
    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        