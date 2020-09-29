from connections import get_connections, DatabaseConnection, encrypt_password


def main():
    databases = get_connections()
    connection = DatabaseConnection(databases["Hermes"])

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
