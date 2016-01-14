import requests
import sys

from accounts.models import ListUser


class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
        # send the assertion to Moz verifier sevice
        data = {'assertion': assertion, 'audience': 'localhost'}
        print('sending to mozilla', data, file=sys.stderr)
        resp = requests.post('https://verifier.login.persona.org/verify',
                             data=data)
        print('got', resp.content, file=sys.stderr)

        # did the verifier respond
        if resp.ok:
            # parse the response
            verification_data = resp.json()

            # check if the assertion was valid
            if verification_data['status'] == 'okay':
                email = verification_data['email']
                try:
                    return self.get_user(email)
                except ListUser.DoesNotExist:
                    return ListUser.objects.create(email=email)

    def get_user(self, email):
        return ListUser.objects.create(email=email)

