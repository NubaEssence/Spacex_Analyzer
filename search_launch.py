import mysql.connector

def search_launch(flight_number):

    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="9082839728",
        database="spacex_analyzer"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM launches WHERE flight_number = %s", (flight_number,))
    result = cursor.fetchone()

    if result:
        print("\n Launch Found:")
        print(f"Flight Number: {result['flight_number']}")
        print(f"Name: {result['name']}")
        print(f"Date (UTC): {result['date_utc']}")
        print(f"Success: {result['success']}")
        print(f"Payloads: {result['payloads']}")
    else:
        print(f"\n No launch found with flight number {flight_number}")

    cursor.close()
    conn.close()


import mysql.connector

def search_launch(flight_number):
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="9082839728",
        database="spacex_analyzer"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM launches WHERE flight_number = %s", (flight_number,))
    result = cursor.fetchone()

    if result:
        print("\nLaunch Found:")
        print(f"Flight Number: {result['flight_number']}")
        print(f"Name: {result['name']}")
        print(f"Date (UTC): {result['date_utc']}")
        print(f"Success: {result['success']}")
        print(f"Payloads: {result['payloads']}")
    else:
        print(f"\n No launch found with flight number {flight_number}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    while True:
        try:
            flight_number = input("\nEnter a flight number: ")

            if flight_number.lower() == "exit":
                print("Goodbye Nuba!")
                break

            flight_number = int(flight_number)
            search_launch(flight_number)

        except ValueError:
            print("Please enter a valid number.")
