from pydantic import Field, BaseModel

class UserSchemaCreate(BaseModel):
    username: str
    email: str
    password: str = Field(min_length=8)