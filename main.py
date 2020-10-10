from connections import DatabaseConnection
from helpers import get_connections


def main():
    master_pass = input('What is your master password (if you don\'t have one run setup.py): ')
    databases = get_connections()

    # pass in your master pass as the second param
    connection = DatabaseConnection(databases["Hermes"], master_pass)

    results = connection.select(
        """
            SELECT *
            FROM contents
            WHERE id = 1;
        """
    )

    print(results)


if __name__ == "__main__":
    main()
