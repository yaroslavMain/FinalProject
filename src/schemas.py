from datetime import datetime
from typing import List

from pydantic import EmailStr, Field
from pydantic.types import Decimal, PositiveInt

from .settings import pwd_context
from .types import Schema


class CommentForm(Schema):
    comment: str = Field(max_length=256)


class CommentArticleSchema(CommentForm):
    user_id: int
    date_created: datetime


class ArticleSchema(Schema):
    name: str
    id: PositiveInt
    slug: str
    description: str
    date_publish: datetime
    image: str
    category_id: int
    comments: List[CommentArticleSchema]


class ProductSchema(Schema):
    id: PositiveInt
    name: str
    price: Decimal
    image: str


class FavoriteSchema(Schema):
    id: PositiveInt
    name: str
    price: Decimal
    image: str


class User(Schema):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        regex=r'(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,64}'
    )

    def hash(self):
        self.password = pwd_context.hash(self.password)


class Token(Schema):
    token_type: str
    access_token: str


class UserFullSchema(User):
    name: str


class UserLoginSchema(User):
    def verify(self, hashed_password: str) -> bool:
        return pwd_context.verify(self.password, hashed_password)
