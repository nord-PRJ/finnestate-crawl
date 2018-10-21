# Finn Real Estate Insight Tool
A real estate tool to gather daily insight on the Norwegian real estate market.

## Getting started
### If you`re running python 3.7 & scrapy 1.5
in order to avoid version error, run: 
```
pip install git+https://github.com/scrapy/scrapy@master --no-dependencies --upgrade
```

## Running the spiders
in order to run the spiders you must run:
```
scrapy crawl <spidername>
```
### Spiders
- finnhomes_top_layer: crawls through Finn.no and grabs all house adds from finn
```
scrapy crawl finnhomes_top_layer
```

### Outputs
You can output the scrape results to a file
- json lines
```
scrapy crawl <spidername> -o <filename>.jl
```
- json
```
scrapy crawl <spidername> -o <filename>.json
```
- csv
```
scrapy crawl <spidername> -o <filename>.csv
```

## Scrapy shell
1. To test selectors use:
```
srapy shell `www.website.com`
```
2. Then try your selector: 
```
>>> response.css('title::text').extract()
```
## Data model