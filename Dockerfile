FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -e .   
RUN pip3 install -r requirements.txt

WORKDIR /usr/src/app/src/diskspacemonitor

EXPOSE 8000

CMD ["uvicorn", "main:app"]