from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='8.8.8.8',port=3000)

def keep_alive():
    t = Thread(target=run)
    t.start()