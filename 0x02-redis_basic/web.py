#!/usr/bin/env python3
"""
Web cache and tracker
"""
import requests
import redis
from functools import wraps

class WebCache:
    def __init__(self):
        self.store = redis.Redis()

    def count_url_access(self, method):
        """ Decorator counting how many times a URL is accessed """
        @wraps(method)
        def wrapper(url):
            cached_key = "cached:" + url
            cached_data = self.store.get(cached_key)
            if cached_data:
                return cached_data.decode("utf-8")

            count_key = "count:" + url
            html = method(url)

            self.store.incr(count_key)
            self.store.set(cached_key, html)
            self.store.expire(cached_key, 10)
            return html
        return wrapper

    @count_url_access
    def get_page(self, url: str) -> str:
        """ Returns HTML content of a url """
        res = requests.get(url)
        return res.text

if __name__ == "__main__":
    web_cache = WebCache()
    url = "http://slowwly.robertomurray.co.uk"
    print(web_cache.get_page(url))
