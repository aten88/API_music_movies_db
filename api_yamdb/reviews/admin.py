from django.contrib import admin

from reviews.models import User, Title, Category, Genre, Review


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'role'
    )
    search_fields = ('email', 'username')
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    empty_value_display = '-пусто-'


admin.site.register((Category, Genre, Review))
