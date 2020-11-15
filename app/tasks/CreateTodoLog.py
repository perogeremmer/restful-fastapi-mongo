from datetime import datetime


from app.models.todo_logs import TodoLogs
from app.tasks.celery_init import app


@app.task
def execute(payload):
    title = payload['todo_title']

    log = TodoLogs()
    log.user = payload['user_id']
    log.todo = payload['todo_id']
    log.created_at = datetime.utcnow()
    log.message = f"Pengguna membuat todo dengan judul {title}"
    log.save()
