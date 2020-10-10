from connections import DatabaseConnection
from helpers import get_connections


def main():
    databases = get_connections()

    hermes_connection = DatabaseConnection(databases["Hermes"])
    migra_connection = DatabaseConnection(databases["Migranova"])

    results = hermes_connection.select(
        """
            SELECT *
            FROM contents
            WHERE id = 1;
        """
    )

    print(results)


if __name__ == "__main__":
    main()
