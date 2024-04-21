import datetime
from .models import Rundown

def validate_rundown_data(rundown_data):
    prev_end_time = datetime.time(0,0)
    for data in rundown_data:
        start_time = data["start_time"].split(":")
        start_time = datetime.time(int(start_time[0]), int(start_time[1]))
        end_time = data["end_time"].split(":")
        end_time = datetime.time(int(end_time[0]), int(end_time[1]))
        if start_time < prev_end_time or start_time >= end_time:
            return False
        prev_end_time = end_time
    return True

def is_valid_updated_data(rundown: Rundown, new_start_time, new_end_time):
    
    if new_end_time <= new_start_time:
        return False
    
    current_order = rundown.rundown_order
    event_id = rundown.event.id
    prev_rundown = Rundown.objects.all().filter(event_id=event_id, rundown_order=current_order-1)
    next_rundown = Rundown.objects.all().filter(event_id=event_id, rundown_order=current_order+1)
    new_start_time = new_start_time.split(":")
    new_start_time = datetime.time(int(new_start_time[0]), int(new_start_time[1]))
    new_end_time = new_end_time.split(":")
    new_end_time = datetime.time(int(new_end_time[0]), int(new_end_time[1]))
    if len(prev_rundown) > 0:
        prev_rundown = prev_rundown[0]
        prev_end_time = prev_rundown.end_time
        if (prev_end_time > new_start_time): 
            return False
    if len(next_rundown) > 0:
        next_rundown = next_rundown[0]
        next_start_time = next_rundown.start_time
        if (next_start_time < new_end_time): 
            return False
    return True