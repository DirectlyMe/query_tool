import yaml
import keyring
import psycopg2 as pg
import pandas as pd
from helpers import get_db_pass


# encapsulate a database connection
class DatabaseConnection:
    # constructor
    def __init__(self, connection_info, **kwargs):
        # if they did provide a password use it
        if (kwargs['master_pass']):
            self.master_pass = kwargs['master_pass']
        # if nothing was provided try to get the password from the keychain
        elif (keyring.get_password('socialchorus_query_tool', 'master_pass')):
            self.master_pass = keyring.get_password('socialchorus_query_tool', 'master_pass')
        # prompt the user for the password if we have nothing to use
        else:
            self.master_pass = input('Enter master password: ')

        self.connection, self.cursor = self.establish_connection(connection_info)
    
    # for 'with' instantiation
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
                password = get_db_pass(connection["db_name"], self.master_pass),
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
            # TODO: add query string validation
            # make sure its actually a select statement

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


    # join two dataframes
    # keys must be unique identifiers
    def join(self, df_one: pd.DataFrame, df_two: pd.DataFrame, df_one_key: str, df_two_key: str) -> pd.DataFrame:
        return df_one.set_index(df_one_key).join(df_two.set_index(df_two_key))
