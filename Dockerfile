# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /todo

COPY requirements.txt /todo/requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0"]

