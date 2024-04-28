FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR .

COPY . .

RUN pip install --upgrade pip  

RUN pip install -r requirements.txt 

EXPOSE 8000
EXPOSE 5432

HEALTHCHECK --interval=15s --timeout=15s --start-period=15s \
    CMD curl --fail http://localhost:8000 || exit 1     

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]