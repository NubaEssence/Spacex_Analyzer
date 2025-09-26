import mysql.connector
from collections import Counter
import matplotlib.pyplot as plt
import os

os.makedirs("static/charts", exist_ok=True)

def fetch_launch_data():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="9082839728",   
        database="spacex_analyzer"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT date_utc, success FROM launches")
    all_launches = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_launches

def plot_success_failure(all_launches):
    success_counts = Counter()
    for launch in all_launches:
        if launch['success']:
            success_counts['Success'] += 1
        else:
            success_counts['Failure'] += 1

    labels = list(success_counts.keys())
    sizes = list(success_counts.values())
    colors = ["#FF6F61", "#00B050"]  
    explode = [0.05, 0.05]

    fig, ax = plt.subplots(figsize=(5, 4), facecolor='none')
    ax.set_facecolor("none")

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct='%1.1f%%', startangle=90,
        colors=colors, explode=explode, shadow=True,
        textprops={'weight': 'bold', 'color': 'white'}
    )

    plt.tight_layout()
    plt.savefig("static/charts/success_failure_pie.png", transparent=True)
    plt.show()
    plt.close()

def plot_launches_per_year(all_launches):
    launches_per_year = Counter()
    for launch in all_launches:
        try:
            year = int(launch['date_utc'][:4])
            launches_per_year[year] += 1
        except:
            continue

    years = sorted(launches_per_year.keys())
    counts = [launches_per_year[y] for y in years]

    fig, ax = plt.subplots(figsize=(5, 4), facecolor='none')
    ax.set_facecolor("none")

    bars = ax.bar(
        years, counts, color="#1E90FF", edgecolor="#0F62FE", linewidth=1.2
    )

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                '%d' % int(height), ha='center', va='bottom',
                fontsize=8, color='white')

    ax.set_xlabel("Year", fontsize=10, weight='bold', color="white")
    ax.set_ylabel("Number of Launches", fontsize=10, weight='bold', color="white")
    ax.tick_params(colors="white")
    ax.grid(axis='y', linestyle='--', alpha=0.3, color="gray")

    plt.tight_layout()
    plt.savefig("static/charts/launches_per_year_bar.png", transparent=True)
    plt.show()
    plt.close()

if __name__ == "__main__":
    launches = fetch_launch_data()
    plot_success_failure(launches)
    plot_launches_per_year(launches)
