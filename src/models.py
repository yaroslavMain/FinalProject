from datetime import datetime

from sqlalchemy import Column, DECIMAL, VARCHAR, INT, ForeignKey, TEXT, BOOLEAN, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    name = Column(VARCHAR(128), nullable=False)
    email = Column(VARCHAR(128), nullable=False, unique=True)
    password = Column(VARCHAR(256), nullable=False)
    is_active = Column(BOOLEAN, default=False)

    def __repr__(self):
        return self.email


class Favorites(Base):
    user_id = Column(INT, ForeignKey('user.id'), nullable=False)
    product_id = Column(INT, ForeignKey('product.id'), nullable=False, unique=True)


class UserEmailVerify(Base):
    id = Column(VARCHAR(128), primary_key=True)
    user_id = Column(INT, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User')


class Product(Base):
    name = Column(VARCHAR(64), nullable=False, unique=True, index=True)
    price = Column(DECIMAL(6, 2), nullable=False)
    image = Column(VARCHAR(256), nullable=False)

    def __repr__(self):
        return self.name


class Category(Base):
    name = Column(VARCHAR(64), nullable=False, unique=True, index=True)
    slug = Column(VARCHAR(64), nullable=False, unique=True, index=True)

    def __repr__(self):
        return self.name


class Article(Base):
    name = Column(VARCHAR(128), nullable=False)
    slug = Column(VARCHAR(64), nullable=False, unique=True, index=True)
    description = Column(TEXT, nullable=False)
    date_publish: datetime = Column(TIMESTAMP)
    image = Column(VARCHAR(256), nullable=False)
    category_id = Column(INT, ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    comments = relationship('ArticleComment')

    def __repr__(self):
        return self.name


class ArticleComment(Base):
    user_id = Column(INT, ForeignKey('user.id'), nullable=False)
    article_id = Column(INT, ForeignKey('article.id'), nullable=False)
    comment = Column(VARCHAR(256), nullable=False)
    date_created: datetime = Column(TIMESTAMP, default=datetime.now())

    def __repr__(self):
        return self.comment


class Testimonial(Base):
    body = Column(VARCHAR(256), nullable=False)
    name = Column(VARCHAR(64), nullable=False)

    def __repr__(self):
        return self.name
