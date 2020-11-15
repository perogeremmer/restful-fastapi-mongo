from starlette.requests import Request
from starlette.responses import JSONResponse

from app import response
from app.models.todo import Todos
from app.tasks import CreateTodoLog
from app.transformers import TodoTransformer


class TodoController:
    @staticmethod
    async def index(request: Request) -> JSONResponse:
        try:
            todos = Todos.objects.all()
            todos = TodoTransformer.transform(todos)
            return response.ok(todos, '')
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def store(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            title = body['title']
            user_id = body['user_id']

            todo = Todos()
            todo.title = title
            todo.owner = user_id
            todo.save()

            todos = TodoTransformer.singleTransform(todo)

            # Menyiapkan payload yang akan dikirim ke worker
            payload = {
                "todo_title": title,
                "user_id": user_id,
                "todo_id": str(todo.id)
            }

            # Menjalankan paylaod
            CreateTodoLog.execute.delay(payload)

            return response.ok(todos, "Berhasil Membuat Todo!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def show(id) -> JSONResponse:
        try:
            todo = Todos.objects(id=id).first()

            if todo is None:
                raise Exception('todo tidak ditemukan!')

            todos = TodoTransformer.singleTransform(todo)
            return response.ok(todos, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def update(id: str, request: Request) -> JSONResponse:
        try:
            body = await request.json()
            title = body['title']
            description = body['description']

            todo = Todos.objects(id=id).first()

            if todo is None:
                raise Exception('todo tidak ditemukan!')

            todo.title = title
            todo.description = description
            todo.save()

            todos = TodoTransformer.singleTransform(todo)
            return response.ok(todos, "Berhasil Mengubah Todo!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def delete(id: str) -> JSONResponse:
        try:
            todo = Todos.objects(id=id).first()

            if todo is None:
                raise Exception('todo tidak ditemukan!')

            todo.delete()
            return response.ok('', "Berhasil menghapusTodo!")
        except Exception as e:
            return response.badRequest('', f'{e}')
