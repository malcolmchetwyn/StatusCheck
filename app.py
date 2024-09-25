from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, validator
from typing import Optional
from datetime import date
import sqlite3
import openai
import os
import re
from dotenv import load_dotenv
import pandas as pd

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

# Load environment variables from .env file
load_dotenv()

# Pydantic model for input validation with optional fields
class StatusCheck(BaseModel):
    date: str
    wake_up_mental: Optional[str] = None
    wake_up_emotional: Optional[str] = None
    wake_up_physical: Optional[str] = None
    post_breakfast_mental: Optional[str] = None
    post_breakfast_emotional: Optional[str] = None
    post_breakfast_physical: Optional[str] = None
    post_breakfast_extra: Optional[str] = None
    post_lunch_mental: Optional[str] = None
    post_lunch_emotional: Optional[str] = None
    post_lunch_physical: Optional[str] = None
    post_lunch_extra: Optional[str] = None
    post_dinner_mental: Optional[str] = None
    post_dinner_emotional: Optional[str] = None
    post_dinner_physical: Optional[str] = None
    post_dinner_extra: Optional[str] = None
    bedtime_mental: Optional[str] = None
    bedtime_emotional: Optional[str] = None
    bedtime_physical: Optional[str] = None
    notes_observations: Optional[str] = None
    exercise_details: Optional[str] = None

    # Validator to replace empty strings with None
    @validator('*', pre=True, always=True)
    def set_empty_string_to_none(cls, v):
        return v or None

# Static files configuration (Optional)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Route to serve the HTML page
@app.get("/")
async def get_status_page(request: Request):
    today = date.today().isoformat()
    return templates.TemplateResponse("statuscheck.html", {"request": request, "date": today})

# Route to serve the status check HTML page
@app.get("/aisummary")
async def get_aisummary_page(request: Request):
    today = date.today().isoformat()
    return templates.TemplateResponse("AIStatusSummary.html", {"request": request, "date": today})

# Mount the static directory to serve the HTML file
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

def fetch_data_from_db(db_file):
    """Fetch data from the SQLite database."""
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query("SELECT * FROM status_checks", conn)
    conn.close()
    return df

# This will store the chat history (keep entire history now)
chat_history = []  # Ensure this is defined outside of any function

@app.post('/chat')
async def chat(request: Request):
    global chat_history  # Declare chat_history as global so that it can be modified

    data = await request.json()
    user_input = data.get('message')

    if not user_input:
        raise HTTPException(status_code=400, detail="Message content is required.")

    # Fetch mood data from the database
    df = fetch_data_from_db(db_file)

    # Define columns for all moods, physical conditions, and additional data, including the date
    columns = [
        'date',  # Add the 'date' field
        'wake_up_mental', 'wake_up_emotional', 'wake_up_physical',
        'post_breakfast_mental', 'post_breakfast_emotional', 'post_breakfast_physical', 'post_breakfast_extra',
        'post_lunch_mental', 'post_lunch_emotional', 'post_lunch_physical', 'post_lunch_extra',
        'post_dinner_mental', 'post_dinner_emotional', 'post_dinner_physical', 'post_dinner_extra',
        'bedtime_mental', 'bedtime_emotional', 'bedtime_physical',
        'notes_observations', 'exercise_details'
    ]

    # Concatenate all the data into a single string, separating different records by a newline
    mood_data = df[columns].fillna('').apply(lambda x: ' | '.join(x), axis=1).str.cat(sep='\n')

    # Append the current user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Keep the full conversation history (remove history length limitation)
    history_as_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])

    if user_input.strip().lower() == 'status report':
        # Prepare the "status report" prompt with the mood data
        prompt = f'''
        You are an exceptionally compassionate and highly experienced psychologist with over 80 years of dedicated clinical practice in mental health, holding a Ph.D. in Clinical Psychology. You specialize in cognitive-behavioral therapy, mood disorders, and have extensive experience training CIA and MI6 clandestine officers and HUMINT (Human Intelligence) officers. Your expertise includes understanding human behavior, interrogation and elicitation techniques, stress management and resilience building, psychological profiling, cross-cultural competence, ethical decision-making, and adaptability training. You are renowned for your empathetic, client-centered approach that fosters a safe and trusting environment. You possess a keen insight into identifying underlying patterns in thoughts, emotions, and behaviors, and you utilize evidence-based strategies tailored to each individual's unique experiences. Your communication style is warm and non-judgmental, demonstrating cultural competence and sensitivity to diverse backgrounds and needs. You are committed to empowering individuals by facilitating personal growth, resilience, and improved mental, emotional, and physical well-being. Your goal:
        
        Analyze the Data:

        Identify key patterns, recurring themes, and significant fluctuations in the client's moods and behaviors.
        Note any correlations between activities, physical states, and emotional well-being.
        
        Provide a Comprehensive Summary and Insights:
        Summarize your findings in an empathetic and understandable manner.
        Highlight any correlations between activities, physical states, and emotional well-being and areas that may need attention or could benefit from positive reinforcement.
        
        Offer Personalized Recommendations:
        Suggest practical and actionable strategies the client can implement to improve their mental, emotional, and physical well-being.
        Ensure the recommendations are evidence-based and tailored to the client's specific experiences and needs.
        Please present your analysis, summary, and recommendations clearly and compassionately, keeping in mind the client's perspective and fostering a supportive tone.

        Here is the data and talk to the person in the first person.

        MOOD DATA: {mood_data}

        THE RESPONSE MUST BE IN MARKDOWN FORMAT ONLY.
        '''
    else:
        # Prepare the prompt with the entire conversation history and mood data

        prompt = f'''

        USER QUESTION: {user_input}


        CONTEXT:
        You are a highly experienced psychologist with dedicated clinical practice in mental health, holding a Ph.D. in Clinical Psychology. 
        You specialize in cognitive-behavioral therapy, mood disorders, and have extensive experience training 
        CIA and MI6 clandestine officers and HUMINT (Human Intelligence) officers. 
        Your expertise includes understanding human behavior, interrogation and elicitation techniques, stress management 
        and resilience building, psychological profiling, 
        cross-cultural competence, ethical decision-making, and adaptability training. You are renowned for your empathetic, 
        client-centered approach that fosters a safe and trusting environment. 
        You possess a keen insight into identifying underlying patterns in thoughts, emotions, and behaviors, 
        and you utilize evidence-based strategies tailored to each individual's unique experiences. 
        Your communication style is warm and non-judgmental, demonstrating cultural competence and 
        sensitivity to diverse backgrounds and needs. You are committed to empowering individuals by facilitating 
        personal growth, resilience, and improved mental, emotional, and physical well-being.

        **Important Instruction:** 
        - Do not refer to the background data unless it is relevant to the response.
        
        BACKGROUND DATA:
        {mood_data}

        THE RESPONSE MUST BE IN MARKDOWN FORMAT ONLY.
        '''

    print(prompt)

    async def generate():
        global chat_history  # Ensure chat_history is global
        try:
            response = await openai.ChatCompletion.acreate(
                model='gpt-4o',
                messages=[
                    {'role': 'system', 'content': "Do not refer to the background data unless it is relevant to the response"},
                    {'role': 'user', 'content': prompt}
                ],
                temperature=0,
                stream=True
            )
            assistant_response = ""  # Initialize the assistant response buffer

            async for chunk in response:
                content = chunk.choices[0].delta.get('content', "")
                if content:
                    assistant_response += content  # Append content to the buffer
                    yield content  # Stream the content back to the user as it is generated

            # Once the entire response is complete, append the full response to chat history
            chat_history.append({"role": "assistant", "content": assistant_response})

        except Exception as e:
            print(e)
            yield f"\n[Error] An error occurred while processing your request. Exception: {e}"

    # Return a StreamingResponse to stream the assistant's response back to the user
    return StreamingResponse(generate(), media_type='text/plain')


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

# POST endpoint to submit a new status
@app.post("/status")
async def submit_status(status: StatusCheck):
    upsert_status(status)
    return {"message": "Status submitted successfully"}

# GET endpoint to fetch today's status
@app.get("/status/today")
async def get_today_status():
    today = date.today().isoformat()
    record = get_status_by_date(today)
    return record or {}

# GET endpoint to fetch status by a specific date
@app.get("/status/{date}")
async def get_status_for_date(date: str):
    record = get_status_by_date(date)
    return record or {}
