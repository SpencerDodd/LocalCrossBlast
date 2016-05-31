# after.py
import time
from deco import concurrent, synchronized

@concurrent
def slow(index):
    time.sleep(5)

@synchronized
def run():
    for index in list('123'):
        slow(index)

run()