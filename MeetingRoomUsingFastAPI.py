from datetime import datetime, timedelta, date, time
from fastapi import FastAPI, HTTPException

app = FastAPI()

booked_slots = []

def is_slot_available(date: date, start_time: datetime, end_time: datetime) -> bool:
    for slot in booked_slots:
        if (
            date == slot['date'] and
            start_time < slot['end_time'] and
            end_time > slot['start_time']
        ):
            return False
    return True

@app.post("/book_slot/")
def book_slot(date_str: str, start_time_str: str, end_time_str: str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(start_time_str, "%H:%M").time()
        end_time_obj = datetime.strptime(end_time_str, "%H:%M").time()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error in date or time: {e}")
    
    if start_time_obj >= end_time_obj:
        raise HTTPException(status_code=400, detail="Start time must be before end time.")
    
    if (datetime.combine(date_obj, end_time_obj) - datetime.combine(date_obj, start_time_obj)).seconds / 3600 != 1:
        raise HTTPException(status_code=400, detail="Slot must be exactly 1 hour long.")
    
    if is_slot_available(date_obj, datetime.combine(date_obj, start_time_obj), datetime.combine(date_obj, end_time_obj)):
        booked_slots.append({
            'date': date_obj,
            'start_time': datetime.combine(date_obj, start_time_obj),
            'end_time': datetime.combine(date_obj, end_time_obj)
        })
        return {"message": "Slot successfully booked!"}
    else:
        raise HTTPException(status_code=400, detail="Time slot is not available.")
