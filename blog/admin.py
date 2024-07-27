from django.contrib import admin
from .models import BlogArticle


@admin.register(BlogArticle)
class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'created_at', 'preview', 'views_count', )
    search_fields = ('title', )
    list_filter = ('created_at', )
