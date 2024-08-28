FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    && apt-get clean

COPY . /app/neogramint

WORKDIR /app/neogramint

RUN pip3 install -r requirements.txt

EXPOSE 27017

CMD ["python3", "neogramint.py"]


