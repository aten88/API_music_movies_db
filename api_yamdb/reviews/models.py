from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # А здесь должен быть кастомный User Санька


class Title(models.Model):
    ''' Модель заглушка требует доработки '''
    # TODO: "Нужно импортировать сюда модель Андрея"
    pass


class Review(models.Model):
    ''' Модель отзыва к произведению '''
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveIntegerField(
        choices=((i, str(i)) for i in range(1, 11)),
        verbose_name='Рейтинг'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ''' Сортируем по дате создания в обр порядке '''
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self) -> str:
        ''' Переопределенный метод строкового представления '''
        return f'Отзыв {self.user.username} к произведению {self.title}'


class Comment(models.Model):
    ''' Модель комментария к отзыву '''
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь'
    )
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ''' Сортируем по дате создания '''
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        ''' Переопределенный метод строкового представления '''
        return f'Комментарий {self.user.username} к отзыву {self.review}'

