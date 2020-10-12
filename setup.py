import keyring
import os
import argparse
from helpers import get_connections, encrypt_password, get_db_pass


# let the user configure the query tool
def setup(args):
    # read all of the databases from the yaml file
    connections = get_connections(args.db_file) if args.db_file else get_connections()

    # make sure the directory that stores the credentials exists
    if (not os.path.isdir('./program_creds')):
        os.mkdir('./program_creds')

    # get the user's master password
    print('\nFirst things first, lets encrypt your passwords.\n')
    master_pass = input(
        'Your passwords will be encrypted with a master password, type it in now: ')

    # store the
    if (str.lower(input('Would you like to store your master password in your OS\'s keychain? (y/n): ')) == 'y'):
        keyring.set_password('socialchorus_query_tool', 'master_pass', master_pass)

    # get and encrypt the password for each database
    for conn, values in connections.items():
        input_pass = input(
            f'\nEnter the password for the {conn} database or enter S to skip: ')

        # check if the user wants to skip setting up this database
        if (str.lower(input_pass) == 's'):
            continue

        # encrypt the password
        encrypted_pass = encrypt_password(input_pass, master_pass)

        creds_file_name = f'./program_creds/{values["db_name"]}_creds'
        # if the credentials file already exists ask if they want to create a new one
        if (os.path.isfile(creds_file_name)):
            if (str.lower(input(f'The credentials file for this database already exists, would you like to delete it and create a new one? (y/n): ')) == 'y'):
                os.remove(creds_file_name)

        # create the file write the password to it so we can read it in when establishing connections
        with open(creds_file_name, 'wb') as f:
            f.write(encrypted_pass)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--db_file', type=str, help='path to database config file')
    args = parser.parse_args()
    setup(args)
