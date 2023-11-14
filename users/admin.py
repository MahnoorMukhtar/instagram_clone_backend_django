from django.contrib import admin

# Register your models here.
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'first_name', 'last_name')
    
admin.site.register(User, UserAdmin)

