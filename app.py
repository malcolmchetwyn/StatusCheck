from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional
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






@app.post("/status")
async def submit_status(status: StatusCheck):
    print(f"Status submitted: {status}")  # Log the submitted data

    # Use the date provided in the request, not today's date
    provided_date = status.date  

    # Check if the CSV file exists; create it if not
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row, including new fields
            writer.writerow([
                "date", "wake_up_mental", "wake_up_emotional", "wake_up_physical",
                "post_breakfast_mental", "post_breakfast_emotional", "post_breakfast_physical", "post_breakfast_extra",
                "post_lunch_mental", "post_lunch_emotional", "post_lunch_physical", "post_lunch_extra",
                "post_dinner_mental", "post_dinner_emotional", "post_dinner_physical", "post_dinner_extra",
                "bedtime_mental", "bedtime_emotional", "bedtime_physical",
                "notes_observations", "exercise_details"
            ])

    # Read existing data from the CSV file
    records = []
    if os.path.exists(csv_file):
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            records = list(reader)

    # Check if a record exists for the provided date and update it
    record_exists = False
    for record in records:
        if record["date"] == provided_date:
            record_exists = True
            record.update({
                "wake_up_mental": status.wake_up_mental or record["wake_up_mental"],
                "wake_up_emotional": status.wake_up_emotional or record["wake_up_emotional"],
                "wake_up_physical": status.wake_up_physical or record["wake_up_physical"],
                "post_breakfast_mental": status.post_breakfast_mental or record["post_breakfast_mental"],
                "post_breakfast_emotional": status.post_breakfast_emotional or record["post_breakfast_emotional"],
                "post_breakfast_physical": status.post_breakfast_physical or record["post_breakfast_physical"],
                "post_breakfast_extra": status.post_breakfast_extra or record["post_breakfast_extra"],  # Ensure new field is updated
                "post_lunch_mental": status.post_lunch_mental or record["post_lunch_mental"],
                "post_lunch_emotional": status.post_lunch_emotional or record["post_lunch_emotional"],
                "post_lunch_physical": status.post_lunch_physical or record["post_lunch_physical"],
                "post_lunch_extra": status.post_lunch_extra or record["post_lunch_extra"],  # Ensure new field is updated
                "post_dinner_mental": status.post_dinner_mental or record["post_dinner_mental"],
                "post_dinner_emotional": status.post_dinner_emotional or record["post_dinner_emotional"],
                "post_dinner_physical": status.post_dinner_physical or record["post_dinner_physical"],
                "post_dinner_extra": status.post_dinner_extra or record["post_dinner_extra"],  # Ensure new field is updated
                "bedtime_mental": status.bedtime_mental or record["bedtime_mental"],
                "bedtime_emotional": status.bedtime_emotional or record["bedtime_emotional"],
                "bedtime_physical": status.bedtime_physical or record["bedtime_physical"],
                "notes_observations": status.notes_observations or record["notes_observations"],
                "exercise_details": status.exercise_details or record["exercise_details"]
            })
            break

    # If no record exists for the provided date, append a new record
    if not record_exists:
        new_record = {
            "date": provided_date,
            "wake_up_mental": status.wake_up_mental,
            "wake_up_emotional": status.wake_up_emotional,
            "wake_up_physical": status.wake_up_physical,
            "post_breakfast_mental": status.post_breakfast_mental,
            "post_breakfast_emotional": status.post_breakfast_emotional,
            "post_breakfast_physical": status.post_breakfast_physical,
            "post_breakfast_extra": status.post_breakfast_extra,  # New field included
            "post_lunch_mental": status.post_lunch_mental,
            "post_lunch_emotional": status.post_lunch_emotional,
            "post_lunch_physical": status.post_lunch_physical,
            "post_lunch_extra": status.post_lunch_extra,  # New field included
            "post_dinner_mental": status.post_dinner_mental,
            "post_dinner_emotional": status.post_dinner_emotional,
            "post_dinner_physical": status.post_dinner_physical,
            "post_dinner_extra": status.post_dinner_extra,  # New field included
            "bedtime_mental": status.bedtime_mental,
            "bedtime_emotional": status.bedtime_emotional,
            "bedtime_physical": status.bedtime_physical,
            "notes_observations": status.notes_observations,
            "exercise_details": status.exercise_details
        }
        records.append(new_record)

    # Write the updated records back to the CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    return {"message": "Status submitted successfully"}
















@app.get("/status/today")
async def get_today_status():
    today = date.today().isoformat()

    if not os.path.exists(csv_file):
        return {}  # Return empty data if the file doesn't exist

    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"] == today:
                return row  # Return today's data if it exists

    return {}  # Return empty data if there's no entry for today

@app.get("/status/{date}")
async def get_status_for_date(date: str):
    print(f"Fetching status for date: {date}")
    if not os.path.exists(csv_file):
        return {}  # Return empty data if the file doesn't exist

    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"] == date:
                return row  # Return the data for the requested date

    return {}  # Return empty data if there's no entry for the requested date
