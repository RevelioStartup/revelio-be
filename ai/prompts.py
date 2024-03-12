import re

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

def create_assistant_prompt(prompt, event):
    if event != None and 'name' in event:
        name = event['name']
    else:
        name = 'unknown'
    
    if event != None and 'theme' in event:
        theme = event['theme']
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
