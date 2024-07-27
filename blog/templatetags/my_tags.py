from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    """
    Шаблонный фильтр, который преобразует переданный путь в полный путь для доступа к медиафайлу.
    """
    if path:
        return f"/media/{path}"
    return "#"
