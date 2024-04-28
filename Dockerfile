FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR .

COPY . .

RUN pip install --upgrade pip  

RUN pip install -r requirements.txt 

EXPOSE 8000
EXPOSE 5432

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]