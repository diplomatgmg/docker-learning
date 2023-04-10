FROM  python:3.9-alpine3.17

COPY req.txt /temp/req.txt
COPY service /service
WORKDIR /service
EXPOSE 8000

RUN pip install -r /temp/req.txt
RUN adduser --disabled-password service-user

USER service-user