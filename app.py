from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
import csv
import os

app = FastAPI()

# Path to store the CSV file
csv_file = "status_checks.csv"

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

class StatusCheck(BaseModel):
    date: str
    wake_up_mental: Optional[str] = Field(None, max_length=100)
    wake_up_emotional: Optional[str] = Field(None, max_length=100)
    wake_up_physical: Optional[str] = Field(None, max_length=100)
    post_breakfast_mental: Optional[str] = Field(None, max_length=100)
    post_breakfast_emotional: Optional[str] = Field(None, max_length=100)
    post_breakfast_physical: Optional[str] = Field(None, max_length=100)
    post_breakfast_extra: Optional[str] = Field(None, max_length=100)  # New field
    post_lunch_mental: Optional[str] = Field(None, max_length=100)
    post_lunch_emotional: Optional[str] = Field(None, max_length=100)
    post_lunch_physical: Optional[str] = Field(None, max_length=100)
    post_lunch_extra: Optional[str] = Field(None, max_length=100)  # New field
    post_dinner_mental: Optional[str] = Field(None, max_length=100)
    post_dinner_emotional: Optional[str] = Field(None, max_length=100)
    post_dinner_physical: Optional[str] = Field(None, max_length=100)
    post_dinner_extra: Optional[str] = Field(None, max_length=100)  # New field
    bedtime_mental: Optional[str] = Field(None, max_length=100)
    bedtime_emotional: Optional[str] = Field(None, max_length=100)
    bedtime_physical: Optional[str] = Field(None, max_length=100)
    notes_observations: Optional[str] = Field(None, max_length=500)
    exercise_details: Optional[str] = Field(None, max_length=500)

# Static files configuration (Optional)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route to serve the HTML page
@app.get("/")
async def get_status_page(request: Request):
    today = date.today().isoformat()
    return templates.TemplateResponse("statuscheck.html", {"request": request, "date": today})

# Utility function to read CSV data
def read_csv_data() -> List[dict]:
    if not os.path.exists(csv_file):
        return []
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Utility function to write CSV data
def write_csv_data(records: List[dict]):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

# Utility function to find a record by date
def find_record_by_date(records: List[dict], record_date: str):
    return next((record for record in records if record["date"] == record_date), None)

@app.post("/status")
async def submit_status(status: StatusCheck):
    records = read_csv_data()

    # Check if a record exists for the provided date and update it
    record = find_record_by_date(records, status.date)
    if record:
        record.update(status.dict(exclude_unset=True))  # Update only the fields that are set
    else:
        records.append(status.dict())

    # Write the updated records back to the CSV file
    write_csv_data(records)
    return {"message": "Status submitted successfully"}

@app.get("/status/today")
async def get_today_status():
    today = date.today().isoformat()
    records = read_csv_data()
    record = find_record_by_date(records, today)
    return record or {}  # Return today's data if it exists, else empty

@app.get("/status/{date}")
async def get_status_for_date(date: str):
    records = read_csv_data()
    record = find_record_by_date(records, date)
    return record or {}  # Return data for the requested date, or empty if not found
