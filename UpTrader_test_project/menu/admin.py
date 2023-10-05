from django.contrib import admin
from menu.models import Menu


class MenuAdmin(admin.ModelAdmin):
    exclude = ('category',)


admin.site.register(Menu, MenuAdmin)
