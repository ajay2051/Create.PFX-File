import base64
import os

import OpenSSL
from django.conf import settings

from .models import ExternalUsers


class TokenVerification:
    def __init__(self, token_string, user) -> None:
        self.token_string = token_string
        self.user = user

    def get_user_certfile(self):
        user_instance = ExternalUsers.objects.filter(user=self.user).first()
        certificate_file_path = user_instance.certificates.certificate_file_path
        password = user_instance.certificates.certificate_password
        return certificate_file_path, password

    def token_verification(self):
        cert_file_path, password = self.get_user_certfile()
        if not cert_file_path or not password:
            return False
        pfx = open(os.path.join(settings.BASE_DIR, cert_file_path), "rb").read()
        p12 = OpenSSL.crypto.PKCS12(pfx, password)
        pk = p12.get_privatekey()
        sign = OpenSSL.crypto.sign(
            pkey=pk,
            data=self.token_string.encode("utf-8"),
            digest="sha256WithRSAEncryption",
        )
        server_token = base64.b64encode(sign).decode("utf-8")
        print(server_token)
        if server_token == self.token_string:
            return True
        return False
