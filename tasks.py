from celery import Celery

import LinkParser
import math
import urllib.request
import redis


# REDIS CONFIGS:
host = "127.0.0.1"
port = "6379"
db = 2
rdb = redis.StrictRedis(host=host, port=port, db=db)

app = Celery('tasks', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/1')


@app.task(rate_limit="1/s")
def download_html(url):
    page = urllib.request.urlopen(url).read()
    stringPage = page.decode('utf-8')
    link_parser(stringPage)
    return page


@app.task(rate_limit="1/s")
def link_parser(page):
    parser = LinkParser.LinkParser()
    parser.feed(page)
    for link in parser.links:
        rdb.incr(link)
        if not rdb.exists(link):
            download_html(link)
