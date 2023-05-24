from django.core import mail
from rest_framework import viewsets, mixins, filters

from api_yamdb.settings import NOREPLY_SERVICE_EMAIL
from api.permissions import IsAdminOrReadOnly


def gen_send_mail(to_email, conf_code):
    """Генерация письма на почту пользователя с кодом подтверждения."""
    subject = 'Код подтверждения от сервиса YaMDB'
    to = to_email
    text_content = f'''Код подтверждения электронной почты от сервиса YaMDB.\n
                       Никому не сообщайте код от вашей учетной записи!\n
                       Код подтверждения: {conf_code}'''
    mail.send_mail(
        subject, text_content,
        NOREPLY_SERVICE_EMAIL, [to],
        fail_silently=False
    )


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CurrentTitleDefault():
    '''Класс для получения поля title из запроса пользователя.'''
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs.get('title_id')

    def __repr__(self):
        return '%s()' % self.__class__.__name__
