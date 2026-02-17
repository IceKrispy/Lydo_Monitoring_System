from django.contrib import admin
from .models import Barangay, Youth


@admin.register(Barangay)
class BarangayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Youth)
class YouthAdmin(admin.ModelAdmin):
    list_display = ('name', 'barangay', 'age', 'program')
    list_filter = ('barangay', 'program', 'gender')
    search_fields = ('name',)
    
# Register your models here.
