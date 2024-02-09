import subprocess


def create_pfx(private_key_file, certificate_file, pfx_file, password=None):
    openssl_cmd = ['openssl', 'pkcs12', '-export', '-out', pfx_file]
    if password:
        openssl_cmd.extend(['-passout', f'pass:{password}'])
    openssl_cmd.extend(['-inkey', private_key_file, '-in', certificate_file])
    subprocess.run(openssl_cmd, check=True)


private_key_path = 'private_key.pem'
certificate_path = 'certificate.pem'
pfx_path = 'certificate.pfx'
passphrase = 'password'

create_pfx(private_key_path, certificate_path, pfx_path, passphrase)

# Create private_key.pem file    openssl genpkey -algorithm RSA -out private_key.pem -aes256

# Generate self-signed certificate file   openssl x509 -req -days 365 -in csr.pem -signkey private_key.pem -out
# certificate.pem
