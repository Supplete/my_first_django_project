from django.contrib import admin

from .models import SparePart

@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'in_stock', 'created_at')
    list_filter = ('in_stock',)
    search_fields = ('name',)