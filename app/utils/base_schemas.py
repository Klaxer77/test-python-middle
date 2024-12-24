from pydantic import BaseModel

class SException(BaseModel):
    detail: str
    
class ValidationErrorDetail(BaseModel):
    loc: list[str] 
    msg: str        
    type: str       

class ErrorResponsePydantic(BaseModel):
    detail: list[ValidationErrorDetail]