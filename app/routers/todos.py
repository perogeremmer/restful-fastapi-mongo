from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.TodoController import TodoController as controller

router = APIRouter()


@router.get("", tags=["todos"])
async def action(request: Request):
    return await controller.index(request)


@router.get("/{id}", tags=["todos"])
async def action(id: str):
    return await controller.show(id)


@router.post("", tags=["todos"])
async def action(request: Request):
    return await controller.store(request)


@router.put("/{id}", tags=["todos"])
async def action(id: str, request: Request):
    return await controller.update(id, request)


@router.delete("/{id}", tags=["todos"])
async def action(id: str):
    return await controller.delete(id)