from pydantic import BaseModel, Field
from datetime import datetime

class SCreateToDo(BaseModel):
    title: str
    
class SListTodo(BaseModel):
    id: int
    title: str
    is_completed: bool
    created_at: datetime
    
class SChangeToDo(BaseModel):
    title: str | None = None
    is_completed: bool | None = Field(default=None)