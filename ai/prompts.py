import re
from event.models import Event

BASE_AUTOFILL_PROMPT = """
You are going to fill data of an event, like objective, theme, and services, where I give you the name, date, and other information

Input is like
name = Class meet
date = 26/02/2024
budget = 1000000
objective = None
attendees = None
theme = Valentine
services = None

based on this, respond with a JSON string. do not give anything other than the JSON string. the JSON has to contain everything from the input. 
Change every None with answer that fits. Do not change other than None. For services, always respond as a list. for example
{"name": "Class meet", "date" = "26/02/2024", "budget":1000000, "objective" : "Meningkatkan keakraban pertemanan antar kelas", "attendees":400, "theme" : "Valentine", "services" :  ["stand makanan", "sound system", "MC"]}

now, respond to this input

"""

BASE_RECOMMENDATION_PROMPT = """
You're going to respond to a prompt about an event. The prompt will ask you to give answer in bullet points.
Breakdown your answer to output, list, and keyword.
Output is your introduction answer, list is the answer in bullet points, keyword is the key of your list.
Keyword should be related to list.

Input is like
prompt = Berikan rekomendasi tempat di Braga, Bandung. Event acara ulang tahun. Tema unknown

based on this, respond with a JSON string. do not give anything other than the JSON string. JSON has to contain output, list, and keyword. For list and keyword, always respond as an array. for example
{"output" : "Berikut adalah rekomendasi tempat untuk acara ulang tahun di Braga, Bandung", "list": ["Braga Art Cafe", "Filosofi Kopi", "We The Fork", "Warung asik", "Sweet Cantina"], "keyword" : ["Cafe Instagrammable Bandung", "Tempat makan Braga", "Cafe Braga nyaman"]}

now, respond to this input

"""

BASE_TASK_STEP_PROMPT = """
You're going to respond to a prompt about a task. The prompt will ask you to give answer in steps. Return at least 4 steps. Each step contains name and description.

name is the name of the step for the task, description is the detailed explanation of the step.

Input is like
event name = Emma's graduation
event theme = Family
task title = Rent photographer
task description = Looking for photographer experienced in graduation photos

based on this, respond with an array JSON string. do not give anything other than JSON string.  for example
{"steps": [{"name": "Search photographer", "description":"Search photographer on social media"}, {"name": "Pay", "description":"Pay photographer before D-Day"}, {"name": "Contact the photographer", "description":"Contact the photographer to give briefing and discuss ideas"}, {"name": "Ask for copies", "description":"Request copies physically on CD and digitally through flash disk"}]}

now, respond to this input

"""

def create_assistant_prompt(prompt, event: Event):
    if event.name:
        name = event.name
    else:
        name = 'unknown'
    
    if event.theme:
        theme = event.theme
    else:
        theme = 'unknown'
    
    full_prompt = f"{BASE_RECOMMENDATION_PROMPT}prompt = {prompt}. Event {name}. Tema {theme}"
    return full_prompt

def create_autofill_prompt(event):

    if len(re.sub(r'[^a-zA-Z0-9\s]', '', event['name']).strip()) == 0:
        return None
    
    prompt_data = ""
    for key, value in event.items():
        prompt_data += f"{str(key)} = {str(value)}\n"
    full_prompt = f"{BASE_AUTOFILL_PROMPT}{prompt_data}"
    return full_prompt

def create_task_steps_prompt(task, event):
    if task.title:
        task_title = task.title
    else:
        return {'"steps": [{"name": "", "description": ""}]'}

    if task.description:
        task_description = task.description
    else:
        return {'"steps": [{"name": "", "description": ""}]'}

    if event.name:
        event_name = event.name
    else:
        event_name = 'unknown'
    
    if event.theme:
        event_theme = event.theme
    else: 
        event_theme = 'unknown'

    full_prompt = f"{BASE_TASK_STEP_PROMPT}event name = {event_name}\nevent theme = {event_theme}\ntask title = {task_title}\ntask description = {task_description}"
    return full_prompt