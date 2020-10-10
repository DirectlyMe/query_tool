import yaml
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


# pull database connections from a yaml file 
def get_connections(conn_file: str = 'databases.yaml') -> dict:
    with open(conn_file) as f:
        return  yaml.load(f, Loader=yaml.FullLoader)


# get the db password from a file
def get_db_pass(db_name: str, master_pass: str) -> str:
    with open(f'./program_creds/{db_name}_creds', 'rb') as f:
        return decrypt_password(f.read(), master_pass).decode('utf-8')


# encrypt a password with a master password and an optional salt
# place the encrypted password in your database.yaml file
def encrypt_password(password: str, master_pass: str, salt: str = 'LSAO195161lasoII') -> bytes:
    hkey = hash_key(master_pass)
    pass_obj = AES.new(hkey, AES.MODE_CFB, salt.encode("utf-8"))
    # encrypt the key and return it
    return pass_obj.encrypt(password.encode('utf-8'))


# decrypt a password with a master password that was used when the password was encrypted
# a custom salt can be provided if desired, it must be 16 bytes
def decrypt_password(encrypted_pass: str, master_pass: str, salt: str = 'LSAO195161lasoII') -> str:
    hkey = hash_key(master_pass)
    pass_obj = AES.new(hkey, AES.MODE_CFB, salt.encode("utf-8"))
    # decrypt the key and return it
    return pass_obj.decrypt(encrypted_pass)


# turn a key in to a 16 byte hash
def hash_key(key: str) -> bytes:
    hash_obj = SHA256.new(key.encode('utf-8'))    
    return hash_obj.digest()
