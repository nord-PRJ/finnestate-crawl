FROM python:3.7-alpine
COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "scrapy crawl finnhomes_top_layer -o init.csv" ]