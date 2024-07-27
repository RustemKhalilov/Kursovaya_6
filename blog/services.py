from django.core.cache import cache

from blog.models import BlogArticle
from config.settings import CACHE_ENABLE


def get_articles_from_cache():
    """
    Получение списка статей блога из кэша. Если кэш пуст,то получение из БД.
    """
    if not CACHE_ENABLE:
        return BlogArticle.objects.all()
    else:
        key = 'categories_list'
        articles = cache.get(key)
        if articles is not None:
            return articles
        else:
            articles = BlogArticle.objects.all()
            cache.set(key, articles)
            return articles
