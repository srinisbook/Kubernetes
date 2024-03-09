FROM python:3.7-alpine

RUN pip install waitress flask requests

RUN mkdir /app

COPY hook.py /app/hook.py

EXPOSE 5000

CMD python /app/hook.py

