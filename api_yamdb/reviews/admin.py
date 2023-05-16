from django.contrib import admin

from .models import Title, Category, Genre


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    empty_value_display = '-пусто-'


admin.site.register((Category, Genre))
