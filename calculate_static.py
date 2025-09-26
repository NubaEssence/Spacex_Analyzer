import requests
import mysql.connector
from collections import Counter
from datetime import datetime

url = "https://api.spacexdata.com/v4/launches"
response = requests.get(url)

if response.status_code == 200:
    launches = response.json()
    print(f"Total launches fetched: {len(launches)}")

    conn = mysql.connector.connect(
        host="localhost",
        port=3306,       
        user="root",          
        password="9082839728",
        database="spacex_analyzer"       
    )
    cursor = conn.cursor()

    for launch in launches:
        flight_number = launch.get("flight_number")
        name = launch.get("name")
        date_utc = launch.get("date_utc")
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

    conn.commit()
    print("Data inserted/updated successfully into MySQL.")

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT date_utc, success FROM launches")
    all_launches = cursor.fetchall()

    # Success vs Failure
    success_counts = Counter()
    for launch in all_launches:
        if launch['success']:
            success_counts['Success'] += 1
        else:
            success_counts['Failure'] += 1

    print("\nSuccess vs Failure Rates:")
    for k, v in success_counts.items():
        print(f"{k}: {v}")

    # Launches per Year
    launches_per_year = Counter()
    for launch in all_launches:
        year = datetime.strptime(launch['date_utc'], "%Y-%m-%dT%H:%M:%S.%fZ").year
        launches_per_year[year] += 1

    print("\nLaunches per Year:")
    for year, count in sorted(launches_per_year.items()):
        print(f"{year}: {count}")

    cursor.close()
    conn.close()

else:
    print("Failed to fetch data:", response.status_code)



