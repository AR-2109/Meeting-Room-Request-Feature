from datetime import datetime, timedelta
booked_slots = []

def is_slot_available(date, start_time, end_time):
    for slot in booked_slots:
        if (date == slot['date'] and 
            start_time < slot['end_time'] and
            end_time > slot['start_time']):
            return False
    return True

def book_slot(date_str, start_time_str, end_time_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()
    except ValueError as e:
        return f"Error in date or time: {e}"
    if start_time >= end_time:
        return "Start time must be before end time."
    if (datetime.combine(date, end_time) - datetime.combine(date, start_time)).seconds / 3600 != 1:
        return "Slot must be exactly 1 hour long."
    if is_slot_available(date, start_time, end_time):
        booked_slots.append({
            'date': date,
            'start_time': datetime.combine(date, start_time),
            'end_time': datetime.combine(date, end_time)
        })
        return "Slot successfully booked!"
    else:
        return "Time slot is not available."
if __name__ == "__main__":
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ")
        start_time_str = input("Enter start time (HH:MM): ")
        end_time_str = input("Enter end time (HH:MM): ")
        
        result = book_slot(date_str, start_time_str, end_time_str)
        print(result)
        
        if result == "Slot successfully booked!":
            break
