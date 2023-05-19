from csv import DictReader
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class Command(BaseCommand):
    help = "Load data from csv to database"

    def handle(self, *args, **options):

        for row in DictReader(open('static/data/users.csv')):
            User.objects.update_or_create(
                id=int(row['id']),
                username=row['username'],
                email=row['email'],
                role=row['role']
            )

        for row in DictReader(open('static/data/category.csv')):
            Category.objects.update_or_create(
                id=int(row['id']),
                name=row['name'],
                slug=row['slug']
            )

        for row in DictReader(open('static/data/genre.csv')):
            Genre.objects.update_or_create(
                id=int(row['id']),
                name=row['name'],
                slug=row['slug']
            )

        for row in DictReader(open('static/data/titles.csv')):
            Title.objects.update_or_create(
                id=int(row['id']),
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(pk=int(row['category']))
            )

        for row in DictReader(open('static/data/review.csv')):
            Review.objects.update_or_create(
                id=int(row['id']),
                title=Title.objects.get(pk=int(row['title_id'])),
                author=User.objects.get(pk=int(row['author'])),
                text=row['text'],
                score=row['score']
            )

        for row in DictReader(open('static/data/comments.csv')):
            Comment.objects.update_or_create(
                id=int(row['id']),
                review=Review.objects.get(pk=int(row['review_id'])),
                author=User.objects.get(pk=int(row['author'])),
                text=row['text']
            )

        for row in DictReader(open('static/data/genre_title.csv')):
            title = Title.objects.get(pk=int(row['title_id']))
            genre = Genre.objects.get(pk=int(row['genre_id']))
            title.genres.add(genre)

        print('Данные успешно добавлены')
