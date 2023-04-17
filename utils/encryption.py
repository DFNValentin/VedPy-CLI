from utils.cryptopass_database import connection
import rsa
import os

dir_keys = 'keys'
dir_location_key = './' + dir_keys

if not os.path.exists(dir_location_key):
    os.mkdir(dir_location_key)
else:
    pass


os.mkdir(dir_location_key)

# Generare key
if os.path.isfile('keys/private_key.pem') and os.path.isfile('keys/public_key.pem'):
    with open('keys/private_key.pem', 'rb') as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read())
    with open('keys/public_key.pem', 'rb') as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
else:
    (public_key, private_key) = rsa.newkeys(2048)
    with open('keys/private_key.pem', 'wb') as f:
        f.write(private_key.save_pkcs1())
    with open('keys/public_key.pem', 'wb') as f:
        f.write(public_key.save_pkcs1())

# Functie encriptare


def encrypt_data(data):
    return rsa.encrypt(data.encode(), public_key)

# Functie decriptare


def decrypt_data(data):
    decrypted_data = rsa.decrypt(data, private_key)
    return decrypted_data.decode('utf-8')

# Obicet pentru cryptare user data


class user_input:
    def __init__(self, app_name, user_name, email, password, id=None):
        self.app_name = app_name
        self.user_name = user_name
        self.email = email
        self.password = password
        self.id = id

    # metoda de criptare
    def encrypt(self):
        self.app_name = encrypt_data(self.app_name)
        self.user_name = encrypt_data(self.user_name)
        self.email = encrypt_data(self.email)
        self.password = encrypt_data(self.password)

    def decrypt(self):
        self.app_name = decrypt_data(self.app_name)
        self.user_name = decrypt_data(self.user_name)
        self.email = decrypt_data(self.email)
        self.password = decrypt_data(self.password)
