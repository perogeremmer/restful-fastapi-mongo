from celery import Celery

from app.tasks import SayHelloWorld

broker_url = 'amqp://guest:guest@localhost:5672/'
redis_broker_url = 'redis://guest:@localhost:6379/'
app = Celery('tasks', backend='rpc://', broker=redis_broker_url)

from celery.schedules import crontab
app.conf.beat_schedule = {
    'say-hello-world': {
        'task': 'app.tasks.celery_init.sayHelloWorld',
        'schedule': crontab(hour=1, minute=3, day_of_week=1)
    },
}


@app.task
def sayHelloWorld():
    SayHelloWorld.execute()