FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY it_events .

#CMD ["gunicorn", "it_events.wsgi:application", "--bind", "0:8000"]
CMD ["python3", "manage.py", "runserver", "0:8000"]