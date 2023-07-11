from fastapi import Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from starlette import status
from starlette.responses import RedirectResponse

from src.settings import templates
from .router import router
from ..models import Testimonial, Product, Category, Article, UserEmailVerify
from ..schemas import ArticleSchema


@router.get(
    '/',
    response_class=HTMLResponse,
    name='main',
    tags=['Site']
)
async def main(request: Request):
    testimonials = await Testimonial.select(select(Testimonial))
    products = await Product.select(
        select(Product)
        .limit(3)
    )

    return templates.TemplateResponse(
        'main/index.html',
        {
            'request': request,
            'testimonials': testimonials,
            'products': products,
        }
    )


@router.get(
    '/shop',
    response_class=HTMLResponse,
    name='shop',
    tags=['Site']
)
async def shop(request: Request):
    return templates.TemplateResponse(
        'main/shop.html',
        {
            'request': request
        }
    )


@router.get(
    '/about',
    response_class=HTMLResponse,
    name='about',
    tags=['Site']
)
async def about(request: Request):
    testimonials = await Testimonial.select(select(Testimonial))

    return templates.TemplateResponse(
        'main/about.html',
        {
            'request': request,
            'testimonials': testimonials,
        }
    )


@router.get(
    '/services',
    response_class=HTMLResponse,
    name='services',
    tags=['Site']
)
async def services(request: Request):
    testimonials = await Testimonial.select(select(Testimonial))
    products = await Product.select(
        select(Product)
        .limit(3)
    )
    return templates.TemplateResponse(
        'main/services.html',
        {
            'request': request,
            'testimonials': testimonials,
            'products': products,
        }
    )


@router.get(
    '/blog',
    response_class=HTMLResponse,
    name='blog',
    tags=['Site']
)
async def blog(request: Request):
    categories = await Category.select(
        select(Category)
        .order_by('id')
    )

    testimonials = await Testimonial.select(select(Testimonial))

    return templates.TemplateResponse(
        'main/blog.html',
        context={
            'request': request,
            'categories': categories,
            'testimonials': testimonials,
        }
    )


@router.get(
    '/article/{article_slug}',
    response_class=HTMLResponse,
    name='article_detail',
    tags=['Site']
)
async def article_detail(request: Request, article_slug: str = Path(max_length=256)):
    with Article.session() as session:
        article = session.scalar(
            select(Article)
            .filter_by(slug=article_slug)
        )

        comments = article.comments

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Article not found')

    return templates.TemplateResponse(
        'main/article-detail.html',
        context={
            'request': request,
            'article': article,
            'comments': comments
        }
    )


@router.get(
    '/login',
    response_class=HTMLResponse,
    name='user_login',
    tags=['Site']
)
async def login(request: Request):
    return templates.TemplateResponse(
        'main/login.html',
        {
            'request': request
        }
    )


@router.get(
    '/register',
    response_class=HTMLResponse,
    name='user_register',
    tags=['Site']
)
async def register(request: Request):
    return templates.TemplateResponse(
        'main/register.html',
        {
            'request': request
        }
    )


@router.get(
    '/verify/{pk}',
    tags=['Site']
)
async def verify(pk: str = Path()):
    with UserEmailVerify.session() as session:
        user = session.get(UserEmailVerify, pk)

        if not user:
            raise HTTPException(400)

        user.user.is_active = True
        session.delete(user)
        session.commit()
        return RedirectResponse('/login')


@router.get(
    '/favorites',
    response_class=HTMLResponse,
    name='favorites',
    tags=['Site']
)
async def favorites(request: Request):
    return templates.TemplateResponse(
        'main/favorites.html',
        {
            'request': request
        }
    )
