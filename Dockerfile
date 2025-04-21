FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080

CMD ["gunicorn", "-b", ":8080", "run:app"]