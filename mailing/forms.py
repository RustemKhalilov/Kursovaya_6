from django import forms
from .models import Client, Mailing, Message


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('owner',)


class ManagerMailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('status',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)

    def clean_title(self):
        cleaned_data = self.cleaned_data['title']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'обман']
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Недопустимое слово в заголовке сообщения!')

        return cleaned_data

    def clean_message(self):
        cleaned_data = self.cleaned_data['message']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'обман']
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Недопустимое слово в сообщении!')

        return cleaned_data
