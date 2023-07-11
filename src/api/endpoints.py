from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import Query, HTTPException, status, Depends
from fastapi.responses import UJSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.models import Product, User, Favorites, Article, UserEmailVerify, ArticleComment, Testimonial
from src.schemas import ProductSchema, Token, UserLoginSchema, ArticleSchema, UserFullSchema, \
    CommentForm
from src.tasks import send_message

from .dependencies import auth, create_token
from .router import router
from ..settings import SETTINGS


@router.post(
    '/login',
    response_model=Token,
    tags=['User'],
    name='login user'
)
async def login(form: UserLoginSchema):
    """
    Аутентификация пользователя.

    :param form: Данные формы входа пользователя.
    :return: Токен доступа.
    """
    user = await User.select(
        select(User)
        .filter_by(email=form.email)
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')

    if not user[0].is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not verify')
    if not form.verify(user[0].password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid password')

    return Token(
        token_type=SETTINGS.TOKEN_TYPE,
        access_token=create_token(user[0].email)
    )


@router.post(
    '/register',
    response_class=UJSONResponse,
    tags=['User'],
    name='register user'
)
async def register(form: UserFullSchema):
    """
    Обработчик HTTP-запроса для регистрации пользователя.

    :param form: Данные формы регистрации пользователя.
    :return: Зарегистрированный пользователь.
    """
    form.hash()
    user = User(**form.dict())
    try:
        await User.save(user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    user_session = UserEmailVerify(id=str(uuid4()), user_id=user.id)
    await UserEmailVerify.save(user_session)

    send_message.delay(
        f'http://127.0.0.1:8000/verify/{user_session.id}',
        user.email
    )
    return user


@router.get(
    '/wishlist',
    tags=['Wishlist'],
    name='get all products from wishlist'
)
async def wishlist(user: User = Depends(auth)):
    """
    Обработчик HTTP-запроса для получения wishlist

    :param user: Пользователь
    :return: Все товары из wishlist
    """
    favorites = await Favorites.select(
        select(Favorites)
        .filter_by(user_id=user.id)
    )
    if not favorites:
        return {'products not found'}
    return [favorite.product_id for favorite in favorites]


@router.post(
    '/wishlist',
    tags=['Wishlist'],
    name='add product to wishlist'
)
async def wishlist(user: User = Depends(auth), product_id: int = Query()):
    """
    Обработчик HTTP-запроса для добавления товара в wishlist

    :param user: Пользователь
    :param product_id: Идентификатор товар
    :return: объект товара
    """
    favourite = Favorites(user_id=user.id, product_id=product_id)
    try:
        await Favorites.save(favourite)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return favourite


@router.delete(
    '/wishlist',
    tags=['Wishlist'],
    name='delete product from wishlist'
)
async def wishlist(user: User = Depends(auth), product_id: int = Query()):
    """
    Обработчик HTTP-запроса для удаления товара в wishlist

    :param user: Пользователь
    :param product_id: Идентификатор товар
    :return: удаленный объект товара
    """
    favorite = await Favorites.select(
        select(Favorites)
        .filter_by(product_id=product_id)
    )
    if not favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    await Favorites.delete(favorite[0])
    return favorite[0]


@router.get(
    '/product',
    response_model=List[ProductSchema],
    tags=['Product'],
    name='get all products'
)
async def product(
        q: str = Query(default=''),
        products_id: List[int] = Query(default=[])
):
    """
    Обработчик HTTP-запроса для получения всех товаров из БД

    :param q: Строка поискового запроса для фильтрации товаров по имени. По умолчанию пустая строка.
    :param products_id: Список идентификаторов товаров для фильтрации. По умолчанию пустой список.
    :return: Список объектов ProductSchema, представляющих найденные товары.
    """
    sql = select(Product).filter(Product.name.contains(q))
    if products_id:
        sql = sql.where(Product.id.in_(products_id))

    products = await Product.select(sql)

    return [ProductSchema.from_orm(product) for product in products]


@router.get(
    '/article',
    response_model=List[ArticleSchema],
    tags=['Article'],
    name='get all articles'
)
async def article(category_id: int = Query(default=0), q: str = Query(default='')):
    """
    Обработчик HTTP-запроса для получения всех статей

    :param category_id: Идентификатор категории (по умолчанию 0 - все категории).
    :param q: Строка поиска для фильтрации статей по имени (по умолчанию пустая строка).
    :return: Список статей, соответствующих указанным параметрам.
    """
    with Article.session() as session:
        sql = select(Article).filter(Article.name.contains(q)).order_by(Article.name)
        if category_id:
            sql = sql.filter_by(category_id=category_id)

        articles = session.scalars(sql)
        return [ArticleSchema.from_orm(article) for article in articles]


@router.post(
    '/comment_article',
    tags=['Article'],
    name='add a comment to an article'
)
async def comment_article(form: CommentForm, user: User = Depends(auth), article_id: int = Query(...)):
    """
    Обработчик HTTP-запроса для добавления комментария к статье

    :param form: Форма комментария с полями comment (текст комментария).
    :param user: Пользователь, отправляющий комментарий.
    :param article_id: Идентификатор статьи, к которой добавляется комментарий. Значение по умолчанию: 1.
    :return: Добавленный комментарий.
    :raises HTTPException: Если происходит ошибка при сохранении комментария вернется статус код 400 (BAD_REQUEST)).
    """
    comment = ArticleComment(user_id=user.id, comment=form.comment, article_id=article_id, date_created=datetime.now())
    try:
        await ArticleComment.save(comment)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return comment


@router.post(
    '/comment',
    tags=['Site'],
    name='add a comment to the site'
)
async def comment(form: CommentForm, user: User = Depends(auth)):
    """
    Обработчик HTTP-запроса для добавления отзыва на платформу

    :param form: Объект CommentForm, содержащий детали комментария.
    :param user: Объект аутентифицированного пользователя.
    :return: Сохраненный объект Testimonial, представляющий добавленный комментарий.
    """
    comment = Testimonial(body=form.comment, name=user.name)
    try:
        await Testimonial.save(comment)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return comment
