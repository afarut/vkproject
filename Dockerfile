FROM python:3.10

RUN apt update --no-install-recommends -y



RUN mkdir /app

WORKDIR /app

EXPOSE 8000

RUN mkdir /app/static

COPY . /app/

RUN pip install -r requirements.txt

CMD ["bash", "run.sh"]

