FROM python:3.9-slim-buster

WORKDIR /src

RUN apt update

RUN pip3 install --upgrade pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src src

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/src

CMD ["python3", "src/main.py"]