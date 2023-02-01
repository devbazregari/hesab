from hesab.celery import app
from time import sleep

@app.task
def my_task():
    sleep(5)
    f = open("demofile333333.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()
    print('hi')
