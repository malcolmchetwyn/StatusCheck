from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date
import sqlite3
import re

app = FastAPI()

# Database file path
db_file = "status_checks.db"

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Initialize SQLite database and create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS status_checks (
            date TEXT PRIMARY KEY,
            wake_up_mental TEXT,
            wake_up_emotional TEXT,
            wake_up_physical TEXT,
            post_breakfast_mental TEXT,
            post_breakfast_emotional TEXT,
            post_breakfast_physical TEXT,
            post_breakfast_extra TEXT,
            post_lunch_mental TEXT,
            post_lunch_emotional TEXT,
            post_lunch_physical TEXT,
            post_lunch_extra TEXT,
            post_dinner_mental TEXT,
            post_dinner_emotional TEXT,
            post_dinner_physical TEXT,
            post_dinner_extra TEXT,
            bedtime_mental TEXT,
            bedtime_emotional TEXT,
            bedtime_physical TEXT,
            notes_observations TEXT,
            exercise_details TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call the function to initialize the database
init_db()

# Pydantic model for input validation
class StatusCheck(BaseModel):
    date: str
    wake_up_mental: Optional[str] = Field(None, max_length=2000)
    wake_up_emotional: Optional[str] = Field(None, max_length=2000)
    wake_up_physical: Optional[str] = Field(None, max_length=2000)
    post_breakfast_mental: Optional[str] = Field(None, max_length=2000)
    post_breakfast_emotional: Optional[str] = Field(None, max_length=2000)
    post_breakfast_physical: Optional[str] = Field(None, max_length=2000)
    post_breakfast_extra: Optional[str] = Field(None, max_length=2000)
    post_lunch_mental: Optional[str] = Field(None, max_length=2000)
    post_lunch_emotional: Optional[str] = Field(None, max_length=2000)
    post_lunch_physical: Optional[str] = Field(None, max_length=2000)
    post_lunch_extra: Optional[str] = Field(None, max_length=2000)
    post_dinner_mental: Optional[str] = Field(None, max_length=2000)
    post_dinner_emotional: Optional[str] = Field(None, max_length=2000)
    post_dinner_physical: Optional[str] = Field(None, max_length=2000)
    post_dinner_extra: Optional[str] = Field(None, max_length=2000)
    bedtime_mental: Optional[str] = Field(None, max_length=2000)
    bedtime_emotional: Optional[str] = Field(None, max_length=2000)
    bedtime_physical: Optional[str] = Field(None, max_length=2000)
    notes_observations: Optional[str] = Field(None, max_length=500)
    exercise_details: Optional[str] = Field(None, max_length=500)

    @validator('*', pre=True, always=True)
    def escape_special_chars(cls, v):
        if isinstance(v, str):
            # Escape quotes and handle backslashes to prevent SQL injection and errors
            # Replace any problematic characters (like pipes, etc.)
            return re.sub(r"[^a-zA-Z0-9\s,.!?\-]", "", v)
        return v

# Static files configuration (Optional)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route to serve the HTML page
@app.get("/")
async def get_status_page(request: Request):
    today = date.today().isoformat()
    return templates.TemplateResponse("statuscheck.html", {"request": request, "date": today})

# Utility function to fetch status by date
def get_status_by_date(record_date: str):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM status_checks WHERE date = ?", (record_date,))
    record = cursor.fetchone()
    conn.close()

    if record:
        # Map the results into a dictionary
        fields = ['date', 'wake_up_mental', 'wake_up_emotional', 'wake_up_physical',
                  'post_breakfast_mental', 'post_breakfast_emotional', 'post_breakfast_physical', 'post_breakfast_extra',
                  'post_lunch_mental', 'post_lunch_emotional', 'post_lunch_physical', 'post_lunch_extra',
                  'post_dinner_mental', 'post_dinner_emotional', 'post_dinner_physical', 'post_dinner_extra',
                  'bedtime_mental', 'bedtime_emotional', 'bedtime_physical', 'notes_observations', 'exercise_details']
        return dict(zip(fields, record))
    return None

# Utility function to add or update a status in the database
def upsert_status(status: StatusCheck):
    # Retrieve existing data for the given date
    existing_record = get_status_by_date(status.date)
    
    # Merge with existing data if available
    if existing_record:
        updated_record = {**existing_record, **status.dict(exclude_unset=True)}
    else:
        updated_record = status.dict(exclude_unset=True)
    
    # Insert or update the record in the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO status_checks (
            date, wake_up_mental, wake_up_emotional, wake_up_physical, 
            post_breakfast_mental, post_breakfast_emotional, post_breakfast_physical, post_breakfast_extra,
            post_lunch_mental, post_lunch_emotional, post_lunch_physical, post_lunch_extra,
            post_dinner_mental, post_dinner_emotional, post_dinner_physical, post_dinner_extra,
            bedtime_mental, bedtime_emotional, bedtime_physical,
            notes_observations, exercise_details
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            wake_up_mental=excluded.wake_up_mental,
            wake_up_emotional=excluded.wake_up_emotional,
            wake_up_physical=excluded.wake_up_physical,
            post_breakfast_mental=excluded.post_breakfast_mental,
            post_breakfast_emotional=excluded.post_breakfast_emotional,
            post_breakfast_physical=excluded.post_breakfast_physical,
            post_breakfast_extra=excluded.post_breakfast_extra,
            post_lunch_mental=excluded.post_lunch_mental,
            post_lunch_emotional=excluded.post_lunch_emotional,
            post_lunch_physical=excluded.post_lunch_physical,
            post_lunch_extra=excluded.post_lunch_extra,
            post_dinner_mental=excluded.post_dinner_mental,
            post_dinner_emotional=excluded.post_dinner_emotional,
            post_dinner_physical=excluded.post_dinner_physical,
            post_dinner_extra=excluded.post_dinner_extra,
            bedtime_mental=excluded.bedtime_mental,
            bedtime_emotional=excluded.bedtime_emotional,
            bedtime_physical=excluded.bedtime_physical,
            notes_observations=excluded.notes_observations,
            exercise_details=excluded.exercise_details
    ''', (
        updated_record['date'], updated_record.get('wake_up_mental'), updated_record.get('wake_up_emotional'), updated_record.get('wake_up_physical'),
        updated_record.get('post_breakfast_mental'), updated_record.get('post_breakfast_emotional'), updated_record.get('post_breakfast_physical'), updated_record.get('post_breakfast_extra'),
        updated_record.get('post_lunch_mental'), updated_record.get('post_lunch_emotional'), updated_record.get('post_lunch_physical'), updated_record.get('post_lunch_extra'),
        updated_record.get('post_dinner_mental'), updated_record.get('post_dinner_emotional'), updated_record.get('post_dinner_physical'), updated_record.get('post_dinner_extra'),
        updated_record.get('bedtime_mental'), updated_record.get('bedtime_emotional'), updated_record.get('bedtime_physical'),
        updated_record.get('notes_observations'), updated_record.get('exercise_details')
    ))
    
    conn.commit()
    conn.close()

@app.post("/status")
async def submit_status(status: StatusCheck):
    upsert_status(status)
    return {"message": "Status submitted successfully"}

@app.get("/status/today")
async def get_today_status():
    today = date.today().isoformat()
    record = get_status_by_date(today)
    return record or {}

@app.get("/status/{date}")
async def get_status_for_date(date: str):
    record = get_status_by_date(date)
    return record or {}
