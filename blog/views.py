from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import BlogArticleForm
from blog.models import BlogArticle
from blog.services import get_articles_from_cache


class BlogArticleCreateView(PermissionRequiredMixin, CreateView):
    """
    Контроллер, который отвечает за создание статьи блога
    """
    model = BlogArticle
    form_class = BlogArticleForm
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.add_blogarticle'

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)


class BlogArticleListView(ListView):
    """
    Контроллер, который отвечает за просмотр списка статей блога
    """
    model = BlogArticle

    def get_queryset(self, *args, **kwargs):
        queryset = get_articles_from_cache().filter(is_published=True)
        return queryset


class BlogArticleDetailView(DetailView):
    """
    Контроллер, который отвечает за просмотр статьи блога
    """
    model = BlogArticle

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogArticleUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Контроллер, который отвечает за редактирование статьи блога
    """
    model = BlogArticle
    form_class = BlogArticleForm
    permission_required = 'blog.change_blogarticle'

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogArticleDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Контроллер, который отвечает за удаление статьи блога
    """
    model = BlogArticle
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_blogarticle'
