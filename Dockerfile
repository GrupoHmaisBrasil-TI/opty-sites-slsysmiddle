FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "/usr/local/bin/uvicorn" ]
CMD [ "--proxy-headers", "--host", "0.0.0.0", "--port", "8000" , "server:app" ]

COPY ./public /public

COPY ./src .