import re

BASE_AUTOFILL_PROMPT = """
You are going to create an objective, theme, and services for an event where I give you the name, date, and budget

Input is like
name = Class meet
date = 26/02/2024
budget = 1000000

based on this, respond with a JSON string. do not give anything other than the JSON string. the JSON has to contain objective, theme, and service. For service, always respond as a list. for example
{"objective" : "Meningkatkan keakraban pertemanan antar kelas", "theme" : "fun sports", "service" :  ["stand makanan", "sound system", "MC"]}

now, respond to this input

"""

def create_autofill_prompt(name, date, budget):
    if len(re.sub(r'[^a-zA-Z0-9\s]', '', name).strip()) == 0:
        return None
    full_prompt = f"{BASE_AUTOFILL_PROMPT}name = {name}\ndate = {date}\nbudget = {budget}"
    return full_prompt
