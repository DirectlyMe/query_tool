import keyring
from helpers import get_connections, encrypt_password, get_db_pass


# let the user configure the query tool
def setup(**kwargs):
    # read all of the databases from the yaml file
    connections = get_connections(kwargs['connfile']) if 'conn_file' in kwargs.values() else get_connections()
    
    # get the user's master password
    print('\nFirst things first, lets encrypt your passwords.\n')
    master_pass = input('Your passwords will be encrypted with a master password, type it in now: ')

    if (input('Would you like to store your master password in your OS\'s keychain? (y/n): ') == 'y'):
        keyring.set_password('system', 'query_tool', master_pass)
    
    # get and encrypt the password for each database
    for conn, values in connections.items():
        password = input(f'\nEnter the password for the {conn} database: ')
        encrypted_pass = encrypt_password(password, master_pass)

        try:
            # create the file write the password to it so we can read it in when establishing connections
            with open(f'./program_creds/{values["db_name"]}_creds', 'wb') as f:
                f.write(encrypted_pass)
        # TODO: if the file already exists ask the user if they want to replace it
        except Exception as error:
            raise Exception(error)
        

if __name__ == "__main__":
    setup()
