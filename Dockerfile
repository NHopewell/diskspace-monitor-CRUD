FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -e .   
RUN pip3 install -r requirements.txt

WORKDIR /usr/src/app/src/diskspacemonitor


CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
