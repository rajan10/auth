from pydantic import BaseModel, Field
from auth.fields import PyObjectId


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=3, description="username of the User")
    password: str = Field(..., min_length=3, description="password of the User")


class UserCreateSchema(UserBaseSchema):
    pass


class UserNameSchema(BaseModel):
    username: str = Field(..., description="username for User when read api is hit")


class UserUpdateSchema(UserBaseSchema):
    pass


class UserDeleteSchema(UserNameSchema):
    pass


class UserSchema(UserBaseSchema):
    id: PyObjectId = Field(..., description="id for user")
