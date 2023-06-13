FROM python:3.10

RUN mkdir /app && mkdir /app/static

WORKDIR /app

EXPOSE 8000

COPY . .

RUN pip install -r requirements.txt

CMD ["bash", "run.sh"]