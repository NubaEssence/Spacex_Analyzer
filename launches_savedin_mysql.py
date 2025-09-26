import requests
import mysql.connector
from datetime import datetime

# 1. Fetch data from SpaceX API
url = "https://api.spacexdata.com/v4/launches"
response = requests.get(url)

if response.status_code == 200:
    launches = response.json()
    print(f"Total launches fetched: {len(launches)}")

    # 2. Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",     
        port=3306,           
        user="root",
        password="9082839728",
        database="spacex_analyzer"
    )
    cursor = conn.cursor()

    # 3. Insert into launches table
    for launch in launches:  
        flight_number = launch.get("flight_number")
        name = launch.get("name")

        # convert date
        date_utc_raw = launch.get("date_utc")
        date_utc = None
        if date_utc_raw:
            date_utc = datetime.fromisoformat(date_utc_raw.replace("Z", "+00:00"))

        success = launch.get("success")
        payloads = ",".join(launch.get("payloads", []))

        cursor.execute("""
            INSERT INTO launches (flight_number, name, date_utc, success, payloads)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                flight_number = VALUES(flight_number),
                name = VALUES(name),
                date_utc = VALUES(date_utc),
                success = VALUES(success),
                payloads = VALUES(payloads)
        """, (flight_number, name, date_utc, success, payloads))

    # 4. Save changes
    conn.commit()
    print("Data inserted/updated successfully into MySQL.")

    # 5. Close connection
    cursor.close()
    conn.close()

else:
    print("Failed to fetch data:", response.status_code)




