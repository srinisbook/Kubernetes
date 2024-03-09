FROM python:3.7.4-alpine

RUN pip install --upgrade pip

RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev

ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "--insecure" , "0.0.0.0:8000"]

