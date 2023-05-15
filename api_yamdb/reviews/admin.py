from django.contrib import admin

from reviews.models import User

@admin.register(User)
class UserAdmi(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'role'
    )
    search_fields = ('email', 'username')
    empty_value_display = '-пусто-'
