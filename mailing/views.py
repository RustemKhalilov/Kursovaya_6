from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.services import get_articles_from_cache
from mailing.forms import ClientForm, MessageForm, MailingForm, ManagerMailingForm
from mailing.models import Message, Log


from django.views.generic import TemplateView

from mailing.models import Mailing, Client


class HomeView(TemplateView):
    """
    Контроллер главной страницы сайта
    """
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailings = Mailing.objects.all()
        clients = Client.objects.all()
        context_data['all_mailings'] = mailings.count()
        context_data['active_mailings'] = mailings.filter(status=Mailing.STARTED).count()
        context_data['active_clients'] = clients.values('email').distinct().count()

        context_data['random_blogs'] = get_articles_from_cache().order_by('?')[:3]
        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечающий за отображение списка клиентов
    """
    model = Client

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер отвечающий за отображение клиента
    """
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер отвечающий за создание клиента
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер отвечающий за редактирование клиента
    """
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:view', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер отвечающий за удаление клиента
    """
    model = Client
    success_url = reverse_lazy('mailing:clients_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечающий за отображение списка сообщений
    """
    model = Message

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер отвечающий за отображение сообщения
    """
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер отвечающий за создание сообщения
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер отвечающий за редактирование сообщение
    """
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('mailing:view_message', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер отвечающий за удаление сообщения
    """
    model = Message
    success_url = reverse_lazy('mailing:messages_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MailingListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечающий за отображение списка рассылок
    """
    model = Mailing

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер отвечающий за отображение рассылки
    """
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager') and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер отвечающий за создание рассылки
    """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailings_list')

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер отвечающий за редактирование рассылки
    """
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:view_mailing', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        """
        Функция, определяющая поля для редактирования в зависимости от прав пользователя
        """
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingForm
        elif user.has_perm('mailing.deactivate_mailing'):
            return ManagerMailingForm
        else:
            raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер отвечающий за удаление расылки
    """
    model = Mailing
    success_url = reverse_lazy('mailing:mailings_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class LogListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечающий за отображение списка попыток рассылок
    """
    model = Log
