from connections import DatabaseConnection
from helpers import get_connections
import argparse


def main(args):
    databases = get_connections()

    hermes_connection = DatabaseConnection(databases["Hermes"])
    migra_connection = DatabaseConnection(databases["Migranova"])

    hermes_results = hermes_connection.select(
        """
            SELECT *
            FROM contents
            WHERE id = 1;
        """
    )

    print(hermes_results)

    migra_results = migra_connection.select(
        """
            SELECT *
            FROM advocates 
            WHERE id = 1;
        """
    )

    print (migra_results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--db_file', type=str, help='path to database config file')
    parser.add_argument('-p', '--master_pass', type=str, help='master password')
    args = parser.parse_args()
    main(args)
