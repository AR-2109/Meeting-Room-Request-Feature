from datetime import datetime, timedelta, date, time
from fastapi import FastAPI, HTTPException
from typing import List

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
        raise HTTPException(status_code=400, detail=f"Error in date or time format: {e}")

    if date_obj > (datetime.now().date() + timedelta(days=10)):
        raise HTTPException(status_code=400, detail="Booking is allowed only up to 10 days in advance.")
    
   
    if start_time_obj >= end_time_obj:
        raise HTTPException(status_code=400, detail="Start time must be before end time.")
    
  
    duration = (datetime.combine(date_obj, end_time_obj) - datetime.combine(date_obj, start_time_obj)).seconds / 3600
    if duration < 1 or duration > 5:
        raise HTTPException(status_code=400, detail="Slot duration must be between 1 to 5 hours.")

   
    start_time = datetime.combine(date_obj, start_time_obj)
    end_time = datetime.combine(date_obj, end_time_obj)
    

    if is_slot_available(date_obj, start_time, end_time):
      
        booked_slots.append({
            'date': date_obj,
            'start_time': start_time,
            'end_time': end_time
        })
        return {"message": "Slot successfully booked!"}
    else:
        raise HTTPException(status_code=400, detail="Time slot is not available due to overlap with an existing booking.")

@app.get("/get_bookings/")
def get_bookings():
    
    return booked_slots

@app.delete("/delete_booking/")
def delete_booking(date_str: str, start_time_str: str, end_time_str: str):

    try:
   
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(start_time_str, "%H:%M").time()
        end_time_obj = datetime.strptime(end_time_str, "%H:%M").time()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error in date or time format: {e}")

    
    start_time = datetime.combine(date_obj, start_time_obj)
    end_time = datetime.combine(date_obj, end_time_obj)
    

    for slot in booked_slots:
        if slot['date'] == date_obj and slot['start_time'] == start_time and slot['end_time'] == end_time:
            booked_slots.remove(slot)
            return {"message": "Booking successfully deleted!"}
    
    raise HTTPException(status_code=404, detail="Booking not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
