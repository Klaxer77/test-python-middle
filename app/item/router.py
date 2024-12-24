from fastapi import APIRouter
from fastapi_cache.decorator import cache
import asyncio
from app.exceptions.item.exceptions import ExcItemNotFound
from app.item.schemas import SChangeToDo, SCreateToDo, SListTodo
from app.item.service import TodoService
from app.utils.base_schemas import SException

router = APIRouter(prefix="/todo", tags=["Item"])


@router.post("", status_code=201)
async def create(user_data: SCreateToDo) -> SListTodo:
    todo = await TodoService.create(title=user_data.title)
    return todo


@router.get("", status_code=200)
@cache(expire=30)  #кэш на 30 секунд
async def find_all() -> list[SListTodo]:
    todos = await TodoService.find_all()
    return todos


@router.get("/{id}", status_code=200, responses={
        404: {"model": SException}
    })
@cache(expire=30) #кэш на 30 секунд
async def find_detail(id: int) -> SListTodo:
    todo = await TodoService.find_one_or_none(todo_id=id)
    if not todo:
        raise ExcItemNotFound
    return todo


@router.put("/{id}", status_code=200, responses={
        404: {"model": SException}
    })
async def change(id: int, user_data: SChangeToDo) -> SListTodo:
    existed_todo = await TodoService.find_one_or_none(todo_id=id)
    
    if not existed_todo:
        raise ExcItemNotFound
    
    modified_todo = await TodoService.change_todo(todo_id=id, user_data=user_data)
    return modified_todo


@router.delete("/{id}", status_code=200, responses={
        404: {"model": SException}
    })
async def delete(id: int) -> SListTodo:
    existed_todo = await TodoService.find_one_or_none(todo_id=id)
    
    if not existed_todo:
        raise ExcItemNotFound
    
    deleted_todo = await TodoService.delete(todo_id=id)
    return deleted_todo

