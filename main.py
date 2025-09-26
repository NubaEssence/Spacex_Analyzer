from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import mysql.connector
from collections import Counter
from datetime import datetime
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database configuration from .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "spacex_analyzer"),
    "auth_plugin": "mysql_native_password"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def fetch_launches(flight_number: str = None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if flight_number:
        cursor.execute("SELECT * FROM launches WHERE flight_number = %s", (flight_number,))
    else:
        cursor.execute("SELECT * FROM launches ORDER BY flight_number ASC")

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    for launch in data:
        try:
            if launch.get("payloads"):
                launch["payloads"] = [p.strip() for p in str(launch["payloads"]).split(",")]
            else:
                launch["payloads"] = []
        except Exception:
            launch["payloads"] = []

    return data

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/charts")
def charts(request: Request):
    return templates.TemplateResponse(
        "charts.html",
        {
            "request": request,
            "success_failure_pie": "/static/charts/success_failure_pie.png",
            "launches_per_year_bar": "/static/charts/launches_per_year.png",
        },
    )

@app.get("/launches")
def launches_page(request: Request):
    all_launches = fetch_launches()
    return templates.TemplateResponse(
        "launches.html", {"request": request, "launches": all_launches, "search": ""}
    )

@app.post("/launches")
def search_launch(request: Request, flight_number: str = Form("")):
    all_launches = fetch_launches(flight_number)
    return templates.TemplateResponse(
        "launches.html",
        {"request": request, "launches": all_launches, "search": flight_number},
    )

@app.get("/stats")
def stats(request: Request):
    all_launches = fetch_launches()

    total = len(all_launches)
    success = sum(
        1 for l in all_launches if str(l.get("success")).lower() in ["1", "true"]
    )
    failure = total - success

    launches_per_year = Counter()

    def parse_year(date_string):
        if not date_string:
            return None
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt).year
            except ValueError:
                continue
        return None

    for l in all_launches:
        year = parse_year(l.get("date_utc"))
        if year:
            launches_per_year[year] += 1

    stats_data = {
        "total": total,
        "success": success,
        "failure": failure,
        "per_year": dict(sorted(launches_per_year.items())),
    }

    return templates.TemplateResponse("stats.html", {"request": request, "stats": stats_data})
