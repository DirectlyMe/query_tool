import yaml
import psycopg2 as pg
import pandas as pd
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2


# pull database connections from a yaml file 
def get_connections(connections_file: str = 'databases.yaml') -> dict:
    with open(connections_file) as f:
        return  yaml.load(f, Loader=yaml.FullLoader)


# encrypt your passwords
def encrypt_password(password: str):
    salt  = b'\x91\x98)2\xe5\x9b\x91S\x90\xbd\xe6\xb4\x15\xf7\x93&Q\xe9PV\xf4\x15r\xcdPa\xca]\xb3\xfb'
    key = PBKDF2(password, salt, dkLen=32) # Your key that you can encrypt with
    print(key)


# encapsulate a database connection
class DatabaseConnection:
    # constructor
    def __init__(self, connection_info):
        self.connection, self.cursor = self.establish_connection(connection_info)
    

    def __enter__(self):
        return self


    # destructor
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
        self.cursor.close()


    # establish and return a connection to a provided database
    def establish_connection(self, connection):
        try:
            est_connection = pg.connect(
                user = connection["user"],
                password = connection["pass"],
                host = connection["url"],
                port = connection["port"],
                database = connection["db_name"])

            # the cursor is what allows us to fire off queries
            cursor = est_connection.cursor()

            # Print PostgreSQL version
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You are connected to - ", record,"\n")

            # return connection object and cursor as a tuple
            return (connection, cursor)
        except (Exception, pg.Error) as error:
            raise Exception(error)


    # provide a helper for a select statement
    def select(self, query: str, pandas = True):
        try:
            if ("SELECT" not in query or "select" not in query):
                 return

            # execute the query and get all rows
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            return results if not pandas else self.to_pandas(results)
        except (Exception, pg.Error) as error:
            raise Exception(error)


    # convert postgres result set to pandas dataframe
    def to_pandas(self, query_results) -> pd.DataFrame:
        # get all the columns in the query
        colnames = [desc[0] for desc in self.cursor.description]
        # generate a dataframe
        return pd.DataFrame(query_results, columns=colnames)


    # join two dataframes helper
    # keys must be unique identifiers
    def join(self, df_one: pd.DataFrame, df_two: pd.DataFrame, df_one_key: str, df_two_key: str) -> pd.DataFrame:
        return df_one.set_index(df_one_key).join(df_two.set_index(df_two_key))
