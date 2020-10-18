from starlette.requests import Request
from starlette.responses import JSONResponse

from app import response
from app.models.user import Users
from app.transformers import UserTransformer


class UserController:
    @staticmethod
    async def index(request: Request) -> JSONResponse:
        try:
            users = Users.objects()
            transformer = UserTransformer.transform(users)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def store(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            name = body['name']

            user = Users(name=name)
            user.save()
            transformer = UserTransformer.singleTransform(user)
            return response.ok(transformer, "Berhasil Membuat User!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def show(id) -> JSONResponse:
        try:
            user = Users.objects.get(id=id)
            transformer = UserTransformer.singleTransform(user)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def update(id: str, request: Request) -> JSONResponse:
        try:
            body = await request.json()
            name = body['name']

            user = Users.objects(id=id).first()
            user.name = name
            user.save()

            transformer = UserTransformer.singleTransform(user)
            return response.ok(transformer, "Berhasil Mengubah User!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def delete(id: str) -> JSONResponse:
        try:
            user = Users.objects(id=id)
            user.delete()
            return response.ok('', "Berhasil Menghapus User!")
        except Exception as e:
            return response.badRequest('', f'{e}')
