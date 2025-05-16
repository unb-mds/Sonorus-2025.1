from pydantic import BaseModel

class UserRegister(BaseModel):
    password: str
    email: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: str
    password: str