from django.db import models


class BlogArticle(models.Model):
    """
    Модель для хранения информации о статье блога
    """
    title = models.CharField(max_length=100, verbose_name="Заголовок", help_text="Введите заголовок статьи")
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    body = models.TextField(verbose_name="Текст статьи", help_text="Введите текст статьи")
    preview = models.ImageField(upload_to="products/photo", verbose_name="Изображение",
                                help_text="Добавьте изображение", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
