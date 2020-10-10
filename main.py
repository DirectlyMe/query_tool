from connections import DatabaseConnection
from helpers import get_connections


def main():
    databases = get_connections()
    
    # pass in your master pass as the second param
    connection = DatabaseConnection(databases["Hermes"], 'Test')

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
