FROM python:3.10-slim

WORKDIR app/src/

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
