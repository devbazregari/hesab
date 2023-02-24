from hesab.celery import app
from time import sleep
from .models import  Debt , User , MessageBox

@app.task
def my_task(data):
    c = User.objects.get(pk=data['creditor_id'])
    debtors_id = [i for i in c.creditor.all() if i.money > data['range']]
    for i in debtors_id:
        MessageBox.objects.create(message="you shoud pay your debt",sender=c,receiver=i.debtor)