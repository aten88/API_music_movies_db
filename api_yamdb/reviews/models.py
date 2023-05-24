from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Переопределенная модель пользователя.
    Добавлены поля bio и confirmation code,
    изменено поле email как обязательное.
    Сделано поле выбора для выбора роли пользователя.
    """

    class Role(models.TextChoices):
        """Класс роли пользователя."""
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name='Имя')
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name='Фамилия'
    )
    password = models.CharField(max_length=128, blank=True, null=True)
    bio = models.TextField(
        blank=True,
        verbose_name='О себе'
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль пользователя'
    )

    class Meta:
        """Сортируем по имени пользователя."""
        ordering = ['username']

    @property
    def is_moderator(self):
        """Метод типа пользователя"""
        return self.role == self.Role.MODERATOR

    @property
    def is_admin(self):
        """Метод типа пользователя"""
        return self.role == self.Role.ADMIN

    def __str__(self):
        ''' Переопределенный метод строкового представления.'''
        return self.username


class Category(models.Model):
    """Модель Категорий."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        unique=True
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        """Сортируем по имени категории."""
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Переопределенный метод строкового представления."""
        return self.name


class Genre(models.Model):
    """Модель Жанров."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        unique=True
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        """Сортируем по имени жанра."""
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """Переопределенный метод строкового представления."""
        return self.name


class Title(models.Model):
    """Модель Произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения')
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска')
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание')
    genres = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    class Meta:
        """Сортируем по имени."""
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Переопределенный метод строкового представления."""
        return self.name


class Review(models.Model):
    """Модель отзыва к произведению."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.PositiveIntegerField(
        choices=((i, str(i)) for i in range(1, 11)),
        verbose_name='Рейтинг'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        """Сортируем по дате создания в обр порядке."""
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_for_title'
            )
        ]

    def __str__(self) -> str:
        """Переопределенный метод строкового представления."""
        return f'Отзыв {self.author.username} к произведению {self.title}'


class Comment(models.Model):
    """Модель комментария к отзыву."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        """Сортируем по дате создания."""
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        """Переопределенный метод строкового представления."""
        return f'Комментарий {self.author.username} к отзыву {self.review}'
